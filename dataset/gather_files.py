# coding=utf-8
# Copyright 2021 Intel Corporation. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import argparse
import logging
import pathlib

from data.BookscorpusTextFormatting import BookscorpusTextFormatting
from data.WikicorpusTextFormatting import WikicorpusTextFormatting

logging.basicConfig(
    format="%(asctime)s - %(levelname)s: %(message)s",
    datefmt="%m/%d/%Y %H:%M:%S",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

FORMATTERS = {"wiki": WikicorpusTextFormatting, "bookcorpus": BookscorpusTextFormatting}

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-f", type=str, required=True, help="Path to extracted wikipedia files or bookcorpus directory"
    )
    parser.add_argument("-o", type=str, required=True, help="Output directory")
    parser.add_argument(
        "--type",
        type=str,
        required=True,
        choices=FORMATTERS.keys(),
        help="Dataset type [wiki, bookcorpus]",
    )
    args = parser.parse_args()

    merged_file = pathlib.Path(args.o, f"{args.type}_one_article_per_line.txt")
    fmt = FORMATTERS.get(args.type)

    if args.type == "wiki":
        data_path = pathlib.Path(args.o, args.type)
        data_path.mkdir(parents=True, exist_ok=True)
    elif args.type == "bookcorpus":
        data_path = pathlib.Path(args.f)

    logger.info(f"Loading {args.type} files and combining into 1 file ...")
    data_formatter = fmt(str(args.f), str(merged_file), recursive=True)
    data_formatter.merge()
    logger.info("Done.")
