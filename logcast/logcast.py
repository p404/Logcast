#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
from cli import LogcastCLI
from config import ConfigLoader

def main():
    with LogcastCLI() as app:
        ConfigLoader()
        app.run()

if __name__ == "__main__":
    main()