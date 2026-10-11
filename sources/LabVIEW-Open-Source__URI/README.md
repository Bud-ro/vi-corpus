# URI
Uniform Resource Identifier


The openURI library is intended to provide basic support for handling RFC3986 Unique Resource Identifiers.
The palette exposes a set of URI composition and decomposition methods that act through regular expressions to manipulate the parts according to the norm.

Official terminology for URIs can be found at https://tools.ietf.org/html/rfc3986

As an example, let's consider the URI below:
https://username:password@tools.ietf.org:443/html/rfc3986?query=test&query2=test2#appendix-A

The library handles decomposition of the URI into its basic components:
* scheme  = https
* authority = username:password@tools.ietf.org:443
* path = "html/rfc3986"
* query = "query=test&query2=test2"
* fragment  = "#appendix-A"

Authority is further decomposable into:
* userinfo = "username:password"
* host = "tools.ietf.org"
* port = "443"

Query can further be decomposed into key-value pairs:
* array of key-value pairs
* 1st pair: key = "query", value = "test"
* 2nd pair: key = "query2", value = "test2"

UTF-8 encoding support from version 1.3.0
* percent-encoding
* html entities

Planned future development includes:

* validation of URIs
* recognition of URN and URL specificities, including IPv4 and IPv6
