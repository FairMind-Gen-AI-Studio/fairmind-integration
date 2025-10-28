#!/usr/bin/env python3
"""
SonarQube Issues Analyzer - User Level Script
Fetches and analyzes SonarQube issues for any project with sonar-project.properties
Automatically detects PR/branch context and fetches appropriate issues
"""

import os
import sys
import json
import requests
import subprocess
from typing import List, Dict, Any, Optional
from datetime import datetime

class SonarQubeAnalyzer:
    def __init__(self, base_url: str, token: str, project_key: str):
        self.base_url = base_url.rstrip('/')
        self.token = token
        self.project_key = project_key
        self.headers = {'Authorization': f'Bearer {token}'}
        
    def get_issues(self, statuses: List[str] = None, severities: List[str] = None, 
                   pull_request: Optional[str] = None, branch: Optional[str] = None) -> List[Dict[str, Any]]:
        """Fetch issues for the project, optionally filtered by PR or branch"""
        if statuses is None:
            statuses = ['OPEN', 'CONFIRMED', 'REOPENED']
        if severities is None:
            severities = ['BLOCKER', 'CRITICAL', 'MAJOR', 'MINOR', 'INFO']
            
        issues = []
        page = 1
        page_size = 500
        
        while True:
            params = {
                'componentKeys': self.project_key,
                'statuses': ','.join(statuses),
                'severities': ','.join(severities),
                'p': page,
                'ps': page_size
            }
            
            # Add PR or branch filter if provided
            if pull_request:
                params['pullRequest'] = pull_request
            elif branch and branch != 'main' and branch != 'master':
                params['branch'] = branch
            
            try:
                response = requests.get(
                    f"{self.base_url}/api/issues/search",
                    headers=self.headers,
                    params=params
                )
                response.raise_for_status()
                data = response.json()
                
                issues.extend(data.get('issues', []))
                
                total = data.get('total', 0)
                if len(issues) >= total or not data.get('issues'):
                    break
                    
                page += 1
                
            except requests.exceptions.RequestException as e:
                print(f"Error fetching issues: {e}", file=sys.stderr)
                break
                
        return issues
    
    def categorize_issues(self, issues: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
        """Categorize issues by severity and type"""
        categorized = {
            'blocker': [],
            'critical': [],
            'major': [],
            'minor': [],
            'info': []
        }
        
        for issue in issues:
            severity = issue.get('severity', 'INFO').lower()
            if severity in categorized:
                categorized[severity].append({
                    'key': issue.get('key'),
                    'type': issue.get('type'),
                    'rule': issue.get('rule'),
                    'message': issue.get('message'),
                    'component': issue.get('component'),
                    'line': issue.get('line'),
                    'effort': issue.get('effort'),
                    'debt': issue.get('debt')
                })
                
        return categorized
    
    def generate_report(self, issues: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate a summary report of issues"""
        categorized = self.categorize_issues(issues)
        
        report = {
            'timestamp': datetime.now().isoformat(),
            'project': self.project_key,
            'total_issues': len(issues),
            'by_severity': {
                severity: len(items) for severity, items in categorized.items()
            },
            'issues': categorized
        }
        
        return report

def get_git_info():
    """Get current Git branch and PR information"""
    branch = None
    pr_number = None
    
    try:
        # Get current branch
        result = subprocess.run(['git', 'branch', '--show-current'], 
                              capture_output=True, text=True, check=False)
        if result.returncode == 0:
            branch = result.stdout.strip()
            
        # Try to get PR number using gh CLI
        if branch:
            result = subprocess.run(['gh', 'pr', 'list', '--head', branch, '--json', 'number', '--jq', '.[0].number'],
                                  capture_output=True, text=True, check=False)
            if result.returncode == 0 and result.stdout.strip():
                pr_number = result.stdout.strip()
    except Exception as e:
        print(f"Warning: Could not get Git/PR info: {e}", file=sys.stderr)
    
    return branch, pr_number

def find_project_root():
    """Find the project root by looking for sonar-project.properties"""
    current_dir = os.getcwd()
    
    # Search upward from current directory
    while current_dir != '/':
        properties_file = os.path.join(current_dir, 'sonar-project.properties')
        if os.path.exists(properties_file):
            return current_dir
        current_dir = os.path.dirname(current_dir)
    
    # If not found upward, check current directory
    if os.path.exists('sonar-project.properties'):
        return os.getcwd()
    
    return None

def main():
    # Find project root
    project_root = find_project_root()
    if not project_root:
        print("Error: No sonar-project.properties file found in current directory or parent directories.", file=sys.stderr)
        print("Please run this command from a project with SonarCloud configured.", file=sys.stderr)
        sys.exit(1)
    
    # Read project key from sonar-project.properties
    project_properties_file = os.path.join(project_root, 'sonar-project.properties')
    project_key = None
    
    with open(project_properties_file, 'r') as f:
        for line in f:
            if line.startswith('sonar.projectKey='):
                project_key = line.split('=', 1)[1].strip()
                break
    
    if not project_key:
        print("Error: sonar.projectKey not found in sonar-project.properties", file=sys.stderr)
        sys.exit(1)
    
    # Configuration uses SonarCloud and environment variables
    config = {
        'base_url': 'https://sonarcloud.io',
        'token': os.getenv('SONAR_TOKEN', ''),
        'project_key': project_key
    }
    
    if not config.get('token'):
        print("Error: SONAR_TOKEN environment variable not found.", file=sys.stderr)
        print("Please set the SONAR_TOKEN environment variable with your SonarCloud token.", file=sys.stderr)
        sys.exit(1)
    
    analyzer = SonarQubeAnalyzer(
        base_url=config['base_url'],
        token=config['token'],
        project_key=config['project_key']
    )
    
    # Get Git context
    branch, pr_number = get_git_info()
    
    # Check if PR exists - this is mandatory
    if not pr_number:
        print(f"⚠️  No pull request found for current branch '{branch}'.", file=sys.stderr)
        print("", file=sys.stderr)
        print("The sonarqube-fix command only works with branches that have an associated pull request.", file=sys.stderr)
        print("Please create a pull request for your branch first, then run this command again.", file=sys.stderr)
        sys.exit(2)  # Exit code 2 to indicate no PR found
    
    # Prepare context message
    context_msg = f"Fetching SonarQube issues for project: {project_key} (PR #{pr_number})"
    print(f"{context_msg}...", file=sys.stderr)
    
    # Fetch issues for the PR only
    issues = analyzer.get_issues(pull_request=pr_number)
    
    if not issues:
        print(f"✅ No open issues found for PR #{pr_number}! Your code is clean.")
        sys.exit(0)
    
    report = analyzer.generate_report(issues)
    
    # Add context to report
    report['context'] = {
        'branch': branch,
        'pull_request': pr_number
    }
    
    # Output JSON report to stdout for Claude to parse
    print(json.dumps(report, indent=2))
    
    # Save to file in project root for reference
    report_file = os.path.join(project_root, 'sonarqube_report.json')
    with open(report_file, 'w') as f:
        json.dump(report, f, indent=2)
    
    print(f"\nReport saved to: {report_file}", file=sys.stderr)
    print(f"Total issues found for PR #{pr_number}: {report['total_issues']}", file=sys.stderr)

if __name__ == "__main__":
    main()