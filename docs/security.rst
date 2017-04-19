.. _security:

=======================
Security considerations
=======================

No security considerations have been taken into mind while writing this
software. The ``AUTH`` implementation will always succeed and no TLS support is
directly available through the cli. It is **strongly** advised to **not** run
this server on a public accessible interface. This was designed to be run in a
dockerized closed network environement.
