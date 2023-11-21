from services.processor import VideoProcessingService

# https://www.youtube.com/watch?v=NsppOR0GzSE&list=PL2LH9u21t_RQC1viFOKJOvUa9aPwi9Aez
# https://www.youtube.com/watch?v=C95QU4JQLsE&list=PLczDDIRnclWRhjOp5nTKZ9NxLlJaDCvkh
# https://www.youtube.com/watch?v=0gpZNfpMBco&list=PLczDDIRnclWRVC1mqWYzumR72-yEBMt8C
# https://www.youtube.com/watch?v=188agVtVMpE&list=PLczDDIRnclWSCTQZrsRLedi4gRSBQYcmB
# https://www.youtube.com/watch?v=EDU4xdlc5Lk&list=PLczDDIRnclWTKHoafzBrZ44MsDn3wRUVQ
# https://www.youtube.com/watch?v=kmXda_CSQnY&list=PLczDDIRnclWSUyL6hBRiv6-k839zhBagO
# https://www.youtube.com/watch?v=I1xfwZ83cEM&list=PLczDDIRnclWRzwqv2KQ7D809RJmlduoJv


def start(url: str):
    VideoProcessingService().process_by_playlist_url(playlist_url=url)


link = input("Enter the YouTube playlist URL: ")
start(link)
