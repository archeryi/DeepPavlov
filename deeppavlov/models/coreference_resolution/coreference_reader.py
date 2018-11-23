# Copyright 2017 Neural Networks and Deep Learning lab, MIPT
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

import os

from os.path import join, exists
from typing import List, Dict
from deeppavlov.core.data.utils import download_decompress
from deeppavlov.core.data.dataset_reader import DatasetReader
from deeppavlov.core.common.registry import register


@register("coreference_reader")
class CorefReader(DatasetReader):

    def read(self, data_path: str, *args, **kwargs) -> Dict[str, List[str]]:
        if exists(data_path):
            dataset = dict()
            for set_ in os.listdir(data_path):
                dataset[set_] = self.read_part(data_path, set_)

            return dataset
        else:
            url = kwargs.get("url")
            if not url:
                # TODO write correct url
                url = ""
            os.makedirs(data_path)
            download_decompress(url, data_path)
            return self.read(join(data_path, "rucor_conll"))

    @staticmethod
    def read_part(data_path, part) -> List[str]:
        if exists(join(data_path, part)):
            documents = []
            for file_name in os.listdir(join(data_path, part)):
                with open(join(data_path, part, file_name), 'r', encoding='utf8') as f:
                    conll_string = f.read()
                    documents.append(conll_string)

            return documents
