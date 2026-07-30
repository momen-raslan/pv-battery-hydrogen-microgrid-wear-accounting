# Weather retrieval and identity

Retrieve the exact fixed TMY input with:

```text
https://re.jrc.ec.europa.eu/api/tmy?lat=31.2&lon=29.919&outputformat=csv
```

Expected identity:

- bytes: `598052`;
- SHA-256:
  `9910a98114157bccaae7091d3e9a51a44a267d8476008722ac6d12c36189b5de`;
- transformation: none.

The bundled `data/alexandria_tmy.csv` was compared byte-for-byte with an
independent response from that official URL during final staging. The
selected source years are also recorded in the CSV footer.
