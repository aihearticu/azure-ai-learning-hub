# Custom Document Intelligence Model - Setup Results

## Storage Account Details
- **Storage Account Name**: ai102form23681
- **Container Name**: sampleforms
- **Resource Group**: rg-james-0951document
- **Location**: East US 2

## SAS URI for Training
```
https://ai102form23681.blob.core.windows.net/sampleforms?se=2026-01-01T00%3A00%3A00Z&sp=rwl&sv=2022-11-02&sr=c&sig=wtUHS8TOKTzjYL%2BlSxH7qhBUOohwpBALgO6g%2Bli20TY%3D
```

## Uploaded Files
- 5 training forms (Form_1.jpg through Form_5.jpg)
- 5 label files defining field locations
- 5 OCR files with text recognition data
- 1 fields.json defining the schema

## Next Steps
Use this SAS URI in the Azure portal or SDK to train a custom Document Intelligence model that can extract specific fields from similar forms.