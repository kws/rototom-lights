import time
import traceback

while True:
    try:
        import rototom
    except Exception as e:
        traceback.print_exception(e, e, e.__traceback__)
        
    print("Finished. Restarting.")
    time.sleep(5)
