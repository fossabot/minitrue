# Minitrue

Miniture is a free nodes collection tool which separate 
'Fetch' and 'Generate' procedure into two parts, allowing to
fetch from the uncensored internet and speed testing from the
censored network.

![GitHub Repo stars](https://img.shields.io/github/stars/WeeksCharrington/minitrue?color=orange&style=for-the-badge)
![Release](https://img.shields.io/github/v/release/WeeksCharrington/minitrue?color=brightgreen&style=for-the-badge)
![License](https://img.shields.io/github/license/WeeksCharrington/minitrue?color=blue&style=for-the-badge)

## Basic Usage

```
python -m pip install './requirements.txt'
python minitrue.py -m [b,d,i] -c [int]
```

## Arguments

* **m**: running mode, d for domestic mode, i for international mode, default(b) for both.
* **c**: total count of the fastest nodes which needed to extract from all nodes, default is 200.
* **h**: show help document.

**For more information, please refer to [Wiki]().**

## Credits

* [mahdibland/V2RayAggregator](https://github.com/mahdibland/V2RayAggregator)
* [tindy2013/subconverter](https://github.com/tindy2013/subconverter)
* [xxf098/LiteSpeedTest](https://github.com/xxf098/LiteSpeedTest)
* [Loyalsoldier/geoip](https://github.com/Loyalsoldier/geoip)
* [All others who kindly share free nodes](https://github.com/WeeksCharrington/minitrue/blob/main/config/sub_list.json)