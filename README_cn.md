
<div align="center">

<h1 align="center" style="display: flex; align-items: center; justify-content: center;">
  <img src="doc2x.svg" width="40" style="margin-right: 15px;">
  <span>Doc2X 文档</span>
</h1>

一些使用 Doc2X API 的示例。

</div>

</br>
</br>

请参考 [飞书](https://noedgeai.feishu.cn/wiki/Q8QIw3PT7i4QghkhPoecsmSCnG1) 以获得更好的阅读体验。

# Python

## requests
使用 `requests` 来使用 API。
- [将 PDF 文件转换为 json](Python/requests/pdf.py)
- [将 PDF 文件转换为 docx](Python/requests/pdf2file.py)

## pdfdeal

[pdfdeal](https://github.com/Menghuan1918/pdfdeal) 是 Doc2X API 的一个封装包
- [将 PDF 文件转换为 docx](Python/pdfdeal/convert_single_pdf.py)
- [将文件夹中的所有 PDF 文件转换为 docx](Python/pdfdeal/convert_folder_pdfs.py)
- [将文件夹中的所有 PDF 文件转换为 docx 和 markdown](Python/pdfdeal/convert_pdfs_multiple_types.py)
- [将文本中HTML格式表格转换为Markdown格式](Python/pdfdeal/html2md.py)，注意由于Markdown表格并不支持合并单元格，因此在有合并单元格(尤其是纵向的合并单元格)时可能会出现数据错位的现象。

## 文本处理

- [将文本中HTML格式表格转换为Markdown格式(使用beautifulsoup4)](Python/texts/html2md.py)，注意由于Markdown表格并不支持合并单元格，因此在有合并单元格(尤其是纵向的合并单元格)时可能会出现数据错位的现象。

# TypeScript

## 文本处理

- [将文本中HTML格式表格转换为Markdown格式](TypeScript/texts/html2md.ts)，注意由于Markdown表格并不支持合并单元格，因此在有合并单元格(尤其是纵向的合并单元格)时可能会出现数据错位的现象。