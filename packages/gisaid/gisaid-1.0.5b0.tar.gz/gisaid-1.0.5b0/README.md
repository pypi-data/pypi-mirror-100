gisaid-uploader
===========================
[![alt text](https://img.shields.io/badge/pypi-1.0.4b0-blue)](https://pypi.org/project/gisaid/) [![alt text](https://img.shields.io/badge/license-MIT-green)](https://github.com/greysonlalonde/gisaid-uploader/blob/main/LICENSE)
  
 Simplified & efficient GISAID interactions.

  
<u><b>** This package is in development **</b></u>
<br>
<br>
Features to be added soon:
- STARLIMS REST API support for pipelines
- GISAID API download functionality

---

1. Register for a [GISAID](https://www.gisaid.org/registration/register/) account

2. Email GISAID & request a client ID  
  
  
Installation:
```python
    >>> pip install gisaid
```

Authenticate once: 

```python
    >>> import gisaid as gs
    >>> gs.GiSaid(authenticate=True, client_id="foo",
    >>>              username="bar", password="foobar", filename="authfile.json")
    "Authentication successful"
```


CSV + fasta file:

```python
    >>> import gisaid as gs
    >>> x = gs.GiSaid("upload.csv", "fasta.fa")
    >>> x.upload()
    "93 Successful Uploads"
    "15 Failed Uploads"
```


Collated CSV:

```python
    >>> import gisaid as gs
    >>> x = gs.GiSaid("collated", "upload.csv")
    >>> x.upload()
    "93 Successful Uploads"
```

Upload to a SQL database:

```python
    >>> import gisaid as gs
    >>> table_name = "foobar"
    >>> method = "append"
    >>> x = gs.GiSaid("upload.csv", "fasta.fa")
    >>> x.upload_sql(table_name, method, conn)
   
```
