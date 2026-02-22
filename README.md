# Packing_Simulator

py3dbp와 plotly를 활용해 패킹 시뮬레이터를 구현했습니다.

# 시연 영상

[streamlit-app-2026-02-20-14-23-07.webm](https://github.com/user-attachments/assets/ac59f853-1775-4b73-8554-4feb0b0bcfaa)

# 사용 방법

아래 링크에서 패킹 시뮬레이션을 사용할 수 있습니다.

https://packingsimulator-inugsiv2jiqwryupgqqetf.streamlit.app/

csv 파일은 아래 형식으로 작성해 주십시오.

| ID | WIDTH | HEIGHT | DEPTH | WEIGHT | QUANTITY |
| :--- | :---: | :---: | :---: | :---: | :---: |
| A | 55 | 30 | 36.6 | 10 | 10 |
| B | 36.6 | 25 | 27.5 | 8 | 10 |
| C | 27.5 | 20 | 22 | 5 | 10 |
| D | 55 | 25 | 27.5 | 12 | 10 |
| E | 110 | 50 | 55 | 25 | 10 |

ID는 상품명, WIDTH는 박스 가로, HEIGHT는 박스 세로, DEPTH는 박스 높이, WEIGHT는 박스 무게, QUANTITY는 박스 수량입니다.

특정 단위를 강제하지 않습니다. 다만, 파레트 설정과 csv 파일에 입력한 수치 단위가 일치해야 합니다.

# 오픈소스

[3D-bin-packing](https://github.com/jerry800416/3D-bin-packing)

중력을 고려한 배치 기능과 아이템의 개별 속성이 추가되어 알고리즘으로 활용했습니다.
