# docker build -t thiesgehrmann/diamond_extract_unaligned:1 ./
FROM python:3

COPY diamond_extract_unaligned.py /usr/bin
RUN chmod +x /usr/bin/diamond_extract_unaligned.py

LABEL maintainer="Thies Gehrmann"

ENTRYPOINT ["/usr/bin/diamond_extract_unaligned.py"]