# diamond_extract_unaligned
Extract the unaligned sequences from a diamond run

A minimal script to extract reads from a FAST[Q/A] File given that diamond was run:
 * With the --unal 1 option
 * default --outfmt settings (this may be updated if demand for it is necessary.

## Usage
```
diamond_extract_unaligned.py [--fqin] [--fqout] [--gzin] [--gzout] <fasta/fastq file> <unaligned_table> <outfile>

  --fqin  Specifies that the input file is fastq
  --fqout Specifies that the output file should be fastq (if input file is fasta, then quality score I will be printed)
  --gzin  Specifies that the input file is gzipped
  --gzout Zpecifies that the output file should be gzipped

```

