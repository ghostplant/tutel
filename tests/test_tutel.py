# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.

import json
import unittest
import sys, subprocess

import GPUtil

class HelloworldCaller():
    """A class for run tutel helloworld example with different arguments"""
    def run(
        self,
        nproc_per_node=1,
        helloworld_file='helloworld',
        top=2, dtype='float32',
        num_local_experts='2',
        hidden_size=2048,
        show_step_time=True
        ):
        """Run helloworld example"""
        if helloworld_file == 'helloworld':
            command = 'python3 -m torch.distributed.launch --nproc_per_node=' + str(nproc_per_node) + ' tutel/examples/helloworld.py --top ' + str(top) + ' --dtype ' + dtype + ' --num_local_experts ' + str(num_local_experts) + ' --hidden_size ' + str(hidden_size)
        if helloworld_file == 'helloworld_megatron':
            command = 'python3 -m torch.distributed.launch --nproc_per_node=' + str(nproc_per_node) + ' tutel/examples/helloworld_megatron.py --dtype ' + dtype + ' --num_local_experts ' + str(num_local_experts) + ' --hidden_size ' + str(hidden_size)
        p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        losses = []
        while p.poll() is None:
            line = p.stdout.readline().decode("utf8").split()
            if len(line) > 5:
                if line[2] == 'loss':
                    if dtype == 'float32':
                        losses.append(round(float(line[4][:-1]), 3))
                    else:
                        losses.append(round(float(line[4][:-1]), 1))
                if show_step_time and line[0] == '[Summary]':
                    print('step time:', line[5])
        p.stdout.close()
        return losses

class TutelTestCase(unittest.TestCase):
    """A class for tutel test cases."""
    def setUp(self):
        """Hook method for setting up the test"""
        self.GPUtype = GPUtil.getGPUs()[0].name
        with open('tests/test_baseline.json') as f:
            self.data = json.load(f)
        for i in range(8):
            for j in range(len(self.data[i]['losses'])):
                if '32' in self.data[i]['dtype']:
                    self.data[i]['losses'][j] = round(float(self.data[i]['losses'][j]), 3)
                else:
                    self.data[i]['losses'][j] = round(float(self.data[i]['losses'][j]), 1)
        self.tutelCaller = HelloworldCaller()

    def test_top1_fp32_1_expert(self):
        """Test helloworld with top1 gate, float32 dtype and 1 expert(s)."""
        for i in range(len(self.data[2]['step_time'])):
            if self.data[2]['step_time'][i]['GPU'] in self.GPUtype:
                print('\nexpected time:', self.data[2]['step_time'][i]['value'])
        self.assertEqual(self.tutelCaller.run(nproc_per_node=1, helloworld_file='helloworld', top=1, dtype='float32', num_local_experts=1), self.data[2]['losses'])

    def test_top1_fp32_2_experts(self):
        """Test helloworld with top1 gate, float32 dtype and 2 expert(s)."""
        for i in range(len(self.data[3]['step_time'])):
            if self.data[3]['step_time'][i]['GPU'] in self.GPUtype:
                print('\nexpected time:', self.data[3]['step_time'][i]['value'])
        self.assertEqual(self.tutelCaller.run(nproc_per_node=1, helloworld_file='helloworld', top=1, dtype='float32', num_local_experts=2), self.data[3]['losses'])

    def test_top1_fp16_1_expert(self):
        """Test helloworld with top1 gate, float16 dtype and 1 expert(s)."""
        for i in range(len(self.data[0]['step_time'])):
            if self.data[0]['step_time'][i]['GPU'] in self.GPUtype:
                print('\nexpected time:', self.data[0]['step_time'][i]['value'])
        self.assertEqual(self.tutelCaller.run(nproc_per_node=1, helloworld_file='helloworld', top=1, dtype='float16', num_local_experts=1)[0:2], self.data[0]['losses'][0:2])

    def test_top1_fp16_2_experts(self):
        """Test helloworld with top1 gate, float16 dtype and 2 expert(s)."""
        for i in range(len(self.data[1]['step_time'])):
            if self.data[1]['step_time'][i]['GPU'] in self.GPUtype:
                print('\nexpected time:', self.data[1]['step_time'][i]['value'])
        self.assertEqual(self.tutelCaller.run(nproc_per_node=1, helloworld_file='helloworld', top=1, dtype='float16', num_local_experts=2)[0:2], self.data[1]['losses'][0:2])

    def test_top2_fp32_1_expert(self):
        """Test helloworld with top2 gate, float32 dtype and 1 expert(s)."""
        for i in range(len(self.data[6]['step_time'])):
            if self.data[6]['step_time'][i]['GPU'] in self.GPUtype:
                print('\nexpected time:', self.data[6]['step_time'][i]['value'])
        self.assertEqual(self.tutelCaller.run(nproc_per_node=1, helloworld_file='helloworld', top=2, dtype='float32', num_local_experts=1), self.data[6]['losses'])

    def test_top2_fp32_2_experts(self):
        """Test helloworld with top2 gate, float32 dtype and 2 expert(s)."""
        for i in range(len(self.data[7]['step_time'])):
            if self.data[7]['step_time'][i]['GPU'] in self.GPUtype:
                print('\nexpected time:', self.data[7]['step_time'][i]['value'])
        self.assertEqual(self.tutelCaller.run(nproc_per_node=1, helloworld_file='helloworld', top=2, dtype='float32', num_local_experts=2), self.data[7]['losses'])

    def test_top2_fp16_1_expert(self):
        """Test helloworld with top2 gate, float16 dtype and 1 expert(s)."""
        for i in range(len(self.data[4]['step_time'])):
            if self.data[4]['step_time'][i]['GPU'] in self.GPUtype:
                print('\nexpected time:', self.data[4]['step_time'][i]['value'])
        self.assertEqual(self.tutelCaller.run(nproc_per_node=1, helloworld_file='helloworld', top=2, dtype='float16', num_local_experts=1)[0:2], self.data[4]['losses'][0:2])

    def test_top2_fp16_2_experts(self): 
        """Test helloworld with top2 gate, float16 dtype and 2 expert(s)."""
        for i in range(len(self.data[5]['step_time'])):
            if self.data[5]['step_time'][i]['GPU'] in self.GPUtype:
                print('\nexpected time:', self.data[5]['step_time'][i]['value'])
        self.assertEqual(self.tutelCaller.run(nproc_per_node=1, helloworld_file='helloworld', top=2, dtype='float16', num_local_experts=2)[0:2], self.data[5]['losses'][0:2])

    def test_compare_megatron_with_tutel(self):
        """Test helloworld_megatron and helloworld which should have same result"""
        self.assertEqual(
            self.tutelCaller.run(nproc_per_node=2, helloworld_file='helloworld', top=2, dtype='float32', num_local_experts=-2, show_step_time=False),
            self.tutelCaller.run(nproc_per_node=2, helloworld_file='helloworld_megatron', dtype='float32', num_local_experts=1, hidden_size=1024, show_step_time=False)
            )