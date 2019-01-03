## 1.9.0 (Unreleased)

IMPROVEMENTS:

- Improve slb vsg by using kwargs ([#23](https://github.com/alibaba/footmark/pull/23))
- Improve slb instance by using kwargs ([#22](https://github.com/alibaba/footmark/pull/22))
- Improve eip connection ([#21](https://github.com/alibaba/footmark/pull/21))
- Merge inner_ip and private_ip, and merge eip and public_ip ([#17](https://github.com/alibaba/footmark/pull/17))

BUG FIXES:

- Fix security token not working bug ([#20](https://github.com/alibaba/footmark/pull/20))

## 1.8.0 (12 November, 2018)

IMPROVEMENTS:

- Add tags for ali_eni ([#16](https://github.com/alibaba/footmark/pull/16))
- Improve network interface ([#15](https://github.com/alibaba/footmark/pull/15))

BUG FIXES:

- Fix eip address and private ip address ([#9](https://github.com/alibaba/footmark/pull/17))

## 1.7.0 (2 November, 2018)

IMPROVEMENTS:

- Add wait time to make sure instance statue is correct ([#13](https://github.com/alibaba/footmark/pull/13))
- Modify security group and rules method ([#12](https://github.com/alibaba/footmark/pull/12))

## 1.6.3 (October 31, 2018)

**Note:** Package 1.6.0-1.6.2 has instanll error and them have been deleted. 1.6.3 is a stable releasse.

IMPROVEMENTS:

- Modify ecs and vpc method 'modify' ([#11](https://github.com/alibaba/footmark/pull/11))
- Add format_vpc_request_kwargs method to make footmark-vpc more automatic ([#10](https://github.com/alibaba/footmark/pull/10))
- Add format_request_kwargs method to make footmark more automatic ([#8](https://github.com/alibaba/footmark/pull/8))

BUG FIXES:

- Fix modify and delete disk bug ([#9](https://github.com/alibaba/footmark/pull/9))

## 1.5.1 (October 19, 2018)

BUG FIXES:

  * Modify setup.py to set the specified sdk version ([#6](https://github.com/alibaba/footmark/pull/6))

## 1.5.0 (July 4, 2018)

IMPROVEMENTS:

  * support network interface management ([#6](https://github.com/alibaba/footmark/pull/6))
  * add new make request method ([#6](https://github.com/alibaba/footmark/pull/6))
  * improve vpc, vswitch and security group ([#6](https://github.com/alibaba/footmark/pull/6))

## 1.3.0 (January 8, 2018)

IMPROVEMENTS:

  * **New Module:** foormark/ecs
  * **New Module:** foormark/ess
  * **New Module:** foormark/oss
  * **New Module:** foormark/rds
  * **New Module:** foormark/slb
  * **New Module:** foormark/vpc
