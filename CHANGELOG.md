## 1.20.0 (Unreleased)

## 1.19.0 (20 March, 2020)
- improve(ecs): support modify instance charge type  ([#73](https://github.com/alibaba/footmark/pull/73))
- improve(disk): When the instance status is not correct, try again ([#71](https://github.com/alibaba/footmark/pull/71))

## 1.18.0 (1 March, 2020)
- Add new module market ([#69](https://github.com/alibaba/footmark/pull/69))

## 1.17.1 (28 February, 2020)
- fix setup error ([#68](https://github.com/alibaba/footmark/pull/68))

## 1.17.0 (27 February, 2020)
- change string to bytes ([#67](https://github.com/alibaba/footmark/pull/67))
- Add new module ram ([#61](https://github.com/alibaba/footmark/pull/61))
- improve method to add or remove tags ([#65](https://github.com/alibaba/footmark/pull/65))

## 1.16.0 (31 January, 2020)

- fix inventory bug ([#63](https://github.com/alibaba/footmark/pull/63))
- improve(rds): modify account and backpolicy ([#60](https://github.com/alibaba/footmark/pull/60))
- improve(slb): Add tags ([#57](https://github.com/alibaba/footmark/pull/57))
- improve (rds): modify rds instance and database ([#53](https://github.com/alibaba/footmark/pull/53))

## 1.15.0 (3 December, 2019)

- Add new module dns ([#50](https://github.com/alibaba/footmark/pull/50))
- improve(ecs): Add run_instances methed ([#46](https://github.com/alibaba/footmark/pull/46))

## 1.14.1 (13 November, 2019)

IMPROVEMENTS:
- modify setup file ([#48](https://github.com/alibaba/footmark/pull/48))

## 1.14.0 (12 November, 2019)
IMPROVEMENTS:

- add modify_route_entry method([#39](https://github.com/alibaba/footmark/pull/39))
- support query instance more than 10 results ([#40](https://github.com/alibaba/footmark/pull/40))
- new module footmark/sts ([#42](https://github.com/alibaba/ansible-provider/pull/42))
- support ecs role name ([#43](https://github.com/alibaba/ansible-provider/pull/43))
- add tags param for vpc module ([#44](https://github.com/alibaba/ansible-provider/pull/44))

## 1.13.0 (October 16, 2019)
IMPROVEMENTS:

- improve code to python3 ([#36](https://github.com/alibaba/footmark/pull/36))
- improve some func's way to pass parameter ([#37](https://github.com/alibaba/footmark/pull/37))

## 1.12.0 (10 July, 2019)

IMPROVEMENTS:

- Publish release 1.12.0 ([#33](https://github.com/alibaba/footmark/pull/33))
- Improve performance of method describe_instances ([#32](https://github.com/alibaba/footmark/pull/32))

## 1.11.0 (12 March, 2019)

BUG FIXES:

- Fix slb server group modifying bug results from data type ([#28](https://github.com/alibaba/footmark/pull/28))

## 1.10.0 (12 March, 2019)

IMPROVEMENTS:

- Improve connection/format_request_kwargs to foramt page_size ([#25](https://github.com/alibaba/footmark/pull/25))

BUG FIXES:

- Fix slb server group modifying bug ([#26](https://github.com/alibaba/footmark/pull/26))

## 1.9.0 (4 January, 2019)

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
