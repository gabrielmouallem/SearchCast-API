from processor.processor import extract_captions;

# main.py
def main():
    captions = extract_captions("https://www.youtube.com/watch?v=LIrUce95RZI")
    print(captions)

if __name__ == "__main__":
    main()
