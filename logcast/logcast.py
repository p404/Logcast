#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
from cli import LogcastCLI

def main():
    with LogcastCLI() as app:
        app.run()

if __name__ == "__main__":
    main()