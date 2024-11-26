function processContent(content: string): string {
    return content.replace(/<table>[\s\S]*?<\/table>/g, (htmlTable) => {
        try {
            // Clean up whitespace and newlines
            const cleanHtml = htmlTable.replace(/\n\s*/g, '');
            const rows = cleanHtml.match(/<tr>(.*?)<\/tr>/g);
            if (!rows) return htmlTable;

            // Parse table data
            let tableData: string[][] = [];
            let maxColumns = 0;

            // Try to convert to markdown table
            try {
                rows.forEach((row, rowIndex) => {
                    if (!tableData[rowIndex]) {
                        tableData[rowIndex] = [];
                    }
                    let colIndex = 0;
                    const cells = row.match(/<td.*?>(.*?)<\/td>/g) || [];

                    cells.forEach((cell) => {
                        while (tableData[rowIndex][colIndex]) {
                            colIndex++;
                        }
                        const colspan = parseInt(cell.match(/colspan="(\d+)"/)?.[1] || '1');
                        const rowspan = parseInt(cell.match(/rowspan="(\d+)"/)?.[1] || '1');
                        const content = cell.replace(/<td.*?>|<\/td>/g, '').trim();

                        for (let i = 0; i < rowspan; i++) {
                            for (let j = 0; j < colspan; j++) {
                                if (!tableData[rowIndex + i]) {
                                    tableData[rowIndex + i] = [];
                                }
                                tableData[rowIndex + i][colIndex + j] = i === 0 && j === 0 ? content : '^^';
                            }
                        }
                        colIndex += colspan;
                        maxColumns = Math.max(maxColumns, colIndex);
                    });

                    for (let i = 0; i < maxColumns; i++) {
                        if (!tableData[rowIndex][i]) {
                            tableData[rowIndex][i] = ' ';
                        }
                    }
                });
                const chunks: string[] = [];

                const headerCells = tableData[0]
                    .slice(0, maxColumns)
                    .map((cell) => (cell === '^^' ? ' ' : cell || ' '));
                const headerRow = '| ' + headerCells.join(' | ') + ' |';
                chunks.push(headerRow);

                const separator = '| ' + Array(headerCells.length).fill('---').join(' | ') + ' |';
                chunks.push(separator);

                tableData.slice(1).forEach((row) => {
                    const paddedRow = row
                        .slice(0, maxColumns)
                        .map((cell) => (cell === '^^' ? ' ' : cell || ' '));
                    while (paddedRow.length < maxColumns) {
                        paddedRow.push(' ');
                    }
                    chunks.push('| ' + paddedRow.join(' | ') + ' |');
                });

                return chunks.join('\n');
            } catch (error) {
                return htmlTable;
            }
        } catch (error) {
            return htmlTable;
        }
    });
}


/*         === Usage ===
Example: Convert HTML table to markdown
*/
const htmlTableExample = `
Table 4: The Transformer generalizes well to English constituency parsing (Results are on Section 23 of WSJ)

<table><tr><td>Parser</td><td>Training</td><td>WSJ 23 F1</td></tr><tr><td>Vinyals & Kaiser el al. (2014) [37]</td><td>WSJ only, discriminative</td><td>88.3</td></tr><tr><td>Petrov et al. (2006) [29]</td><td>WSJ only, discriminative</td><td>90.4</td></tr><tr><td>Zhu et al. (2013) [40]</td><td>WSJ only, discriminative</td><td>90.4</td></tr><tr><td>Dyer et al. (2016) [8]</td><td>WSJ only, discriminative</td><td>91.7</td></tr><tr><td>Transformer (4 layers)</td><td>WSJ only, discriminative</td><td>91.3</td></tr><tr><td>Zhu et al. (2013) [40]</td><td>semi-supervised</td><td>91.3</td></tr><tr><td>Huang & Harper (2009) [14]</td><td>semi-supervised</td><td>91.3</td></tr><tr><td>McClosky et al. (2006) [26]</td><td>semi-supervised</td><td>92.1</td></tr><tr><td>Vinyals & Kaiser el al. (2014) [37]</td><td>semi-supervised</td><td>92.1</td></tr><tr><td>Transformer (4 layers)</td><td>semi-supervised</td><td>92.7</td></tr><tr><td>Luong et al. (2015) [23]</td><td>multi-task</td><td>93.0</td></tr><tr><td>Dyer et al. (2016) [8]</td><td>generative</td><td>93.3</td></tr></table>
`;

const markdownTable = processContent(htmlTableExample);
console.log(markdownTable);
/* Output:
Table 4: The Transformer generalizes well to English constituency parsing (Results are on Section 23 of WSJ)

| Parser | Training | WSJ 23 F1 |
| --- | --- | --- |
| Vinyals & Kaiser el al. (2014) [37] | WSJ only, discriminative | 88.3 |
| Petrov et al. (2006) [29] | WSJ only, discriminative | 90.4 |
| Zhu et al. (2013) [40] | WSJ only, discriminative | 90.4 |
| Dyer et al. (2016) [8] | WSJ only, discriminative | 91.7 |
| Transformer (4 layers) | WSJ only, discriminative | 91.3 |
| Zhu et al. (2013) [40] | semi-supervised | 91.3 |
| Huang & Harper (2009) [14] | semi-supervised | 91.3 |
| McClosky et al. (2006) [26] | semi-supervised | 92.1 |
| Vinyals & Kaiser el al. (2014) [37] | semi-supervised | 92.1 |
| Transformer (4 layers) | semi-supervised | 92.7 |
| Luong et al. (2015) [23] | multi-task | 93.0 |
| Dyer et al. (2016) [8] | generative | 93.3 |
*/