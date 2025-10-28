const pptxgen = require('pptxgenjs');
const html2pptx = require('/Users/alexiocassani/.claude/plugins/marketplaces/anthropic-agent-skills/document-skills/pptx/scripts/html2pptx.js');

async function createPresentation() {
    const pptx = new pptxgen();
    pptx.layout = 'LAYOUT_16x9';
    pptx.author = 'Fairmind';
    pptx.title = 'Fairmind-Claude Code Integration - Complete';

    // Original slides
    await html2pptx('workspace/slide1.html', pptx);
    await html2pptx('workspace/slide2.html', pptx);
    await html2pptx('workspace/slide3.html', pptx);
    await html2pptx('workspace/slide4.html', pptx);

    // New detailed skill slides
    await html2pptx('workspace/slide5-fairmind-context.html', pptx);
    await html2pptx('workspace/slide6-fairmind-tdd.html', pptx);
    await html2pptx('workspace/slide7-fairmind-code-review.html', pptx);

    // Save presentation
    await pptx.writeFile({ fileName: 'fairmind-claude-agents-workflows-complete.pptx' });
    console.log('Complete presentation created successfully with 7 slides!');
}

createPresentation().catch(console.error);
