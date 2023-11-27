from services.processor.processor_service import VideoProcessingService

playlist_urls = [
    "https://www.youtube.com/watch?v=qlmUwgTy97M&list=PLWieWKZeFoVQQzBATfDAmHaLgA3Sf5p0O&pp=iAQB",
    "https://www.youtube.com/watch?v=b_V8DaBQdZc&list=PLWieWKZeFoVQlGQ98RT2Qk4ToKTLPcY71&pp=iAQB",
    "https://www.youtube.com/watch?v=RGRPikhvsfw&list=PLWieWKZeFoVQBl5jPTEvWUah6-FTufaKi&pp=iAQB",
    "https://www.youtube.com/watch?v=gvRPQtjWi-g&list=PLWieWKZeFoVRmUNn9KA2dVpQswo19QkwQ&pp=iAQB",
    "https://www.youtube.com/watch?v=Cko3pI9ulo4&list=PLWieWKZeFoVSLVo0Bn5UdlUdsuz21CXcF&pp=iAQB",
    "https://www.youtube.com/watch?v=8Zaon08OH4w&list=PLaE_mZALZ0V2E0lVJowee_oerd3OMvyJu&pp=iAQB",
    "https://www.youtube.com/watch?v=qbTzhB0akt8&list=PLJznpI7w9Top6QMp_VIJ55AX0XKHNxS6m&pp=iAQB",
    "https://www.youtube.com/watch?v=EMoz7L-d22E&list=PLJznpI7w9TooV0ORuL9e4ZRYMznV_Dwdp&pp=iAQB",
    "https://www.youtube.com/watch?v=NsppOR0GzSE&list=PL2LH9u21t_RQC1viFOKJOvUa9aPwi9Aez&pp=iAQB",
    "https://www.youtube.com/watch?v=__X8Oi39c2c&list=PL2LH9u21t_RTCiui6rC6Wq1th3AuFiyuF&pp=iAQB",
    "https://www.youtube.com/watch?v=U3ophUXNdNM&list=PL2LH9u21t_RQHH8-d83KgE3l8PpgsCJfO&pp=iAQB",
    "https://www.youtube.com/watch?v=TP_L8BJ-oiM&list=PL2LH9u21t_RRWELTLdCQ5pQCb0DH8E8Jt&pp=iAQB",
    "https://www.youtube.com/watch?v=RwcKSWQftsc&list=PL2LH9u21t_RRuy-phww2UsZSCjwMvg6bI&pp=iAQB",
    "https://www.youtube.com/watch?v=4MUhBxNvM6g&list=PL2LH9u21t_RQem8hD6JsCb2Sur7mdkpnf&pp=iAQB",
    "https://www.youtube.com/watch?v=zd3aiBnRmWM&list=PL2LH9u21t_RT9x3qBV7_-mkgAbKKw9i-d&pp=iAQB",
    "https://www.youtube.com/watch?v=AN3idqDG9l0&list=PL2LH9u21t_RTT9LjbyT2A68Nl85vrN2o-&pp=iAQB",
    "https://www.youtube.com/watch?v=lQRC306DC08&list=PL2LH9u21t_RQiHUnXSNCP_H73NzXg-PgH&pp=iAQB",
    "https://www.youtube.com/watch?v=HDKN-xLr8w8&list=PL2LH9u21t_RRqov7qUsZE-_srSoLRuTYg&pp=iAQB",
    "https://www.youtube.com/watch?v=hu4c5oV3RaY&list=PL2LH9u21t_RRPwZ4USb7gliQy6bVXRPng&pp=iAQB",
    "https://www.youtube.com/watch?v=qkjJzReuWDE&list=PL2LH9u21t_RSuTFNq2F0sVDNK-rF7Aeje&pp=iAQB",
    "https://www.youtube.com/watch?v=PF2SEjknoQQ&list=PL2LH9u21t_RR9rA0r0BhySZPJmU7xoUm_&pp=iAQB",
    "https://www.youtube.com/watch?v=-6hHmEJyFDM&list=PLczDDIRnclWRAi9rLUxxUHz2j7XSEothf&pp=iAQB",
    "https://www.youtube.com/watch?v=j5Erz8kZsWQ&list=PLczDDIRnclWQn9afuQsVri7alTiB6xkYp&pp=iAQB",
    "https://www.youtube.com/watch?v=I1xfwZ83cEM&list=PLczDDIRnclWRzwqv2KQ7D809RJmlduoJv&pp=iAQB",
    "https://www.youtube.com/watch?v=C95QU4JQLsE&list=PLczDDIRnclWRhjOp5nTKZ9NxLlJaDCvkh&pp=iAQB",
    "https://www.youtube.com/watch?v=AiJ1LB-RC8A&list=PLczDDIRnclWQsxDtnqeMYhZ-2gaORWOdv&pp=iAQB",
    "https://www.youtube.com/watch?v=PD92_0cQvOo&list=PLByCI4BxQvkSJKS_sj01Vg_5kuyBO3bsq&pp=iAQB",
    "https://www.youtube.com/watch?v=m_N3N51Gy7M&list=PLiN2MRmKAem7_MAihEI8pDxcEcVw9CqDJ",
    "https://www.youtube.com/watch?v=c31_h9b4Se4&list=PLiN2MRmKAem4QRKJmgvVh24TN7k4fWWq_",
    "https://www.youtube.com/watch?v=BT5tFJ9tHro&list=PLiN2MRmKAem5BVg97wKfgJ9ykN_yxGbs8",
]


# def start(url: str):
def start():
    VideoProcessingService().process_by_playlist_urls(
        playlist_urls=playlist_urls, max_videos_per_channel=10
    )


# link = input("Enter the YouTube playlist URL: ")
# start(link)
start()
