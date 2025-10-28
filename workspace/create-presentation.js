const pptxgen = require('pptxgenjs');
const html2pptx = require('/Users/alexiocassani/.claude/plugins/marketplaces/anthropic-agent-skills/document-skills/pptx/scripts/html2pptx.js');

async function createPresentation() {
    const pptx = new pptxgen();
    pptx.layout = 'LAYOUT_16x9';
    pptx.author = 'Fairmind';
    pptx.title = 'Fairmind-Claude Code Integration';

    // Slide 1: The Agent Ecosystem
    await html2pptx('workspace/slide1.html', pptx);

    // Slide 2: The Skills Framework
    await html2pptx('workspace/slide2.html', pptx);

    // Slide 3: Key Workflows Enabled
    await html2pptx('workspace/slide3.html', pptx);

    // Slide 4: Integration Architecture & Value
    await html2pptx('workspace/slide4.html', pptx);

    // Save presentation
    await pptx.writeFile({ fileName: 'fairmind-claude-agents-workflows.pptx' });
    console.log('Presentation created successfully!');
}

createPresentation().catch(console.error);
