# -*- coding: utf-8 -*-
version = '0.5.4'

# 필요한 최소 hunspell 버전.
# - 코드에서는 if config.minimum_hunspell_version >= (1,2,14): 와 같이
#   사용 가능
minimum_hunspell_version = (1,2,14)

# 보조용언 붙여 쓴 형태 모두 사전에 기재, 거짓이면 합성어 형태로 사용
# - 장점: hunspell의 합성어 기능의 문제점과 한계를 피해갈 수 있다
# - 단점: 사전이 몇 배로 커져서 처리 속도가 느려 진다.
expand_auxiliary_attached = True
