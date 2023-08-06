# Python MRO Language Server

A simple Python language server to provide **MRO** (Method Resolution Order) inference.

**MRO** is the order in which Python looks for a method in a hierarchy of classes. Python uses *C3 Linearisation* [(wiki page)](https://en.wikipedia.org/wiki/C3_linearization) as the underlying algorithm.

This project conforms to Microsoft's [Language Server Protocol](https://microsoft.github.io/language-server-protocol/) but only support Hover and CodeLens requests. Python 3.6+ are supported.

![Continuous Integration Status](https://github.com/mosckital/python-mro-language-server/workflows/Continuous%20Integration/badge.svg)
[![GitHub license](https://img.shields.io/github/license/mosckital/python-mro-language-server.svg)](https://github.com/mosckital/python-mro-language-server/blob/master/LICENSE)

## Installation

The Python MRO language server can be easily installed by:

```shell
pip install python-mro-language-server
```

The language server uses `jedi` for static syntax analysis and `python-jsonrpc-server` for the JsonRPC communications. These two packages and their dependencies, `ujson` and `parso`, will be installed by the about command as well.

## Usage

The Python MRO language server can be launched by the following command:

```shell
python -m mrols.server [port]
```

Where `port` is 3000 by default if not specified.

## Language Server Features

The main purpose of this language server is to *infer and return the MRO of a target in request* via static syntax analysis of the provided source codes.

By static syntax analysis, there is a minimum level of security risk since the source codes will not be run. This is at the expense that the inference may be incomplete in some situations, like when using a dynamically declared type or having no information about the external library. However, the user can expect that the inference should work in a large part of the common cases.

The necessary static syntax analysis is achieved by using both the [`jedi`](https://github.com/davidhalter/jedi) analysis library and the Python built-in library `ast` (stands for Abstract Syntax Trees). The `jedi` library is in primary use and the `ast` library provides additional supports.

### Hover functionality

The Python MRO Language Server implements the [**Hover Request**](https://microsoft.github.io/language-server-protocol/specifications/specification-current/#textDocument_hover) of the Language Server Protocol. The user can fetch the MRO list of a class or its instance by hovering over the class name (implemented) or instance name (to implement very soon).

### CodeLens functionality

The Python MRO Language Server implements the [**Code Lens Request**](https://microsoft.github.io/language-server-protocol/specifications/specification-current/#textDocument_codeLens) and the [**Code Lens Resolve Request**](https://microsoft.github.io/language-server-protocol/specifications/specification-current/#codeLens_resolve) as well. A code lens will appear at the first line of every class declaration. The user can get the MRO list of the declared class by clicking the code lens.

## Relation to the Python MRO extension for VS Code

This language server is the backend server used in the [Python MRO](https://github.com/mosckital/vscode_python_mro) extension for VS Code.

It is very welcomed that this language server can be used in any other extensions to any editor that supports the Language Server Protocol.

## Incoming Features

The following list includes the features to add into the Python MRO Language Server in the next releases.

* New Features:
  * Hover:
    * add support to show MRO list when hovering over a class instance
    * add support to show the which class in the MRO list will provide the actual implementation when hovering over a method of a class instance (lower priority, scheduled after finishing the other features)
  * CodeLens:
    * change the way to show MRO list when clicking a code lens from showing in a pop-up message window to showing in a side panel like [what GitLens does](https://github.com/eamodio/vscode-gitlens#git-code-lens-).
* Project Reliability
  * increase the readability of the documentations
  * add coverage check and show the result as a badge in README
  * add pylint check and show the score as a badge in README
  * add logging to the whole scope of the project and save the last logs in file

## Contribution

Any contribution is welcomed!
