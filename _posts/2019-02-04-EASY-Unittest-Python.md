---
layout: post 
title: Python Unittest
date: 2022-01-04 16:20:23 +0900 
category: Python 
tag: Python 
---


### * Sample Class (Person Class):

```python
class Person ():
    name_ls = []

    def set_name(self, new_name: str):
        self.name_ls.append (new_name)
        return len (self.name_ls) - 1  # returning index

    def get_name(self, ind: int):
        if ind < len (self.name_ls):
            return self.name_ls[ind]
        else:
            return None


if __name__ == '__main__':
    myperson = Person ()

    print ('User xyz has been added with id ', myperson.set_name ('xyz'))
    print ('User abc has been added with id ', myperson.set_name ('abc'))

    print ('User associated with id 0 is ', myperson.get_name (0))
    print ('User associated with id 1 is ', myperson.get_name (1))

    print ('User associated with id 0 is ', myperson.get_name (17))
    print (myperson.name_ls)
```


### * Sample Unittest Class (PersonTest.py):

```python
import Person as PersonClass
import unittest

class Test (unittest.TestCase):
    po = PersonClass.Person ()
    test_name_ls = []
    sample_ind_ls = []

    def test_0_set_name(self):  # Caution: test_(execution_index_must)_fname()
        for i in range (5):
            local_name = str (i) * 2
            test_ind = self.po.set_name (new_name=local_name)
            self.assertIsNotNone (test_ind)
            self.test_name_ls.append (local_name)
            self.sample_ind_ls.append (test_ind)

    def test_1_get_name(self):  # test_(execution_index_must)_f()
        for ind, nname in enumerate(self.test_name_ls):
            self.assertEqual (nname, self.po.get_name (ind))


if __name__ == '__main__':
    unittest.main ()
```

### Output: 


```shell
============================= test session starts ==============================
collecting ... collected 2 items

PersonTest.py::Test::test_0_set_name PASSED                              [ 50%]
PersonTest.py::Test::test_1_get_name PASSED                              [100%]

============================== 2 passed in 0.01s ===============================
```



