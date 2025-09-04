# TCP(Transport Control Protocol)

## 3-way handshake

TCP에서 연결을 시작할 때 하는 과정

1. SYN (synchronize)
    - 클라이언트 → 서버
    - “나 연결하고 싶어! 그리고 내 시퀀스 번호는 X야.”

    여기서 시퀀스 번호(sequence number)는 송신자가 데이터를 순서대로 주고받기 위해 찍는 번호표 같은 것.

2. SYN-ACK (synchronize-acknowledge)
    - 서버 → 클라이언트
    > “좋아, 네 요청 받았어. 네 X도 확인했고, 내 시퀀스 번호는 Y야.”
    - 서버는 클라이언트의 SYN에 대한 ACK(응답 확인)를 보내고, 자기 것도 새로 SYN으로 던진다.

3. ACK (acknowledge)
    - 클라이언트 → 서버
    >“오케이, 네 Y 확인했어. 이제 진짜 데이터 주고받자.”
    - 클라이언트가 서버의 SYN에 대한 ACK을 보내면서 연결이 확립됨.
