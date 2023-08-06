# Necessity

> "Ale is my bear necessity."

# Usage

```python
>>> from necessity import count_column, sample_by_percentile

>>> data = ['foo'] * 100 + ['bar'] * 20 + ['blah'] * 50
>>> data += ['abc'] * 30 + ['xyz'] * 20 + ['bear'] * 10
>>> df = pd.DataFrame({'things': data})

>>> count_columns(df, 'things', normalize=True)
foo     0.434783
blah    0.217391
abc     0.130435
xyz     0.086957
bar     0.086957
bear    0.043478
Name: things, dtype: float64

>>> sample_by_percentile(df, 'things',bins=[0.0, 0.25, 0.75, 1.0], sample_sizes=[2, 1, 1])
['bear', 'bar', 'abc', 'foo']
```
