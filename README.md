# hunspell 한국어 데이터, 개발 정보

프로젝트 정보: https://spellcheck-ko.github.io/

Github 프로젝트: https://github.com/spellcheck-ko/hunspell-dict-ko/

갈퀴 단어 정보: https://galkwi.pyok.org/

이 프로젝트는 2017년부터 공개SW개발자Lab의 지원을 받고 있습니다.
(http://kosslab.kr)

## 이용하기

이 곳에는 소스 코드가 들어 있습니다. 맞춤법 검사 기능을 사용하려면
OS별 패키지를 설치하시거나, 여러 가지 애플리케이션별 확장 기능을
이용하십시오. 또는 빌드한 사전 파일을 사용할 수도 있습니다.

 * 데비안: hunspell-ko 패키지 설치, 6.0 (squeeze) 이후 패키지 정보
 * 우분투: hunspell-ko 패키지 설치, 9.10 (karmic) 이후 패키지 정보
 * 페도라: hunspell-ko 패키지 설치, fc12 이후 패키지 정보

 * Mac OS X 10.5: BaramSpellChecker
 * Mac OS X 10.6 이상: /Library/Spelling 또는 홈폴더/Library/Spelling 아래 aff/dic 파일 복사 
 * Mozilla/Firefox 부가 기능
 * LibreOffice 및 OpenOffice.org 부가 기능 

사전 파일은 ko.aff 파일과 ko.dic 파일 2개로 이루어져 있고 hunspell
사전이 저장되는 위치에 복사해 사용할 수도 있습니다.

## hunspell 버전 정보

ko.dic 파일에는 표제어 데이터가 들어 있고 ko.aff (affix) 파일에는
단어의 활용 정보가 들어갑니다. aff 파일과 dic 파일은 hunspell의 전신인
myspell에서도 이용하는 형식이지만 한국어 데이터는 hunspell에만 들어
있는 기능이 필요하기 때문에 hunspell에서만 동작합니다.

 * 현재의 모든 기능을 사용하려면 hunspell 1.2.14 이상 버전이 필요합니다.
   * hunspell 1.6.0 버전은 버그로 대치어의 인코딩이 잘못됩니다. 1.4.x 이하 또는 1.6.1 이상 버전을 사용하십시오.
 * 대부분의 최근 OS와 애플리케이션은 이보다 높은 버전을 사용하고 있으나, 예외적으로 맥오에스에 내장된 hunspell은 1.2.8을 사용하고 있습니다.
 * hunspell 1.2.8에서는 이상 동작을 막기 위해 1.2.8용으로 빌드한 aff 및 dic 파일이 필요합니다. 단 일부 동작하지 않는 기능이 있습니다.
 * hunspell 커맨드라인에서 사용할 경우 1.2.11 이전 버전은 한글 단어 분리를 제대로 하지 못해 동작하지 않습니다.
 * 최근 버전에서도 알려진 문제점으로 hunspell 커맨드라인에서 사용할 때 '+' 기호로 시작하는 어근이 제대로 변환되지 않습니다.
