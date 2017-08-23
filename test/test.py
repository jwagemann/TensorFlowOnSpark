import os
import unittest

from pyspark import SparkContext
from pyspark.sql import SparkSession

class SparkTest(unittest.TestCase):
  """Base class for unittests using Spark.  Sets up and tears down a cluster per test class"""

  @classmethod
  def setUpClass(cls):
    master = os.getenv('MASTER')
    assert master is not None, "Please start a Spark standalone cluster and export MASTER to your env."

    num_workers = os.getenv('SPARK_WORKER_INSTANCES')
    assert num_workers is not None, "Please export SPARK_WORKER_INSTANCES to your env."

    cls.num_workers = int(num_workers)
    cls.sc = SparkContext(master, cls.__name__)
    cls.spark = SparkSession.builder.getOrCreate()

  @classmethod
  def tearDownClass(cls):
    cls.spark.stop()
    cls.sc.stop()


class SimpleTest(SparkTest):
  """Check that basic Spark is working"""
  def test_spark(self):
    sum = self.sc.parallelize(range(1000)).sum()
    self.assertEqual(sum, 499500)


if __name__ == '__main__':
  unittest.main()
