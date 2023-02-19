import subprocess
import shlex


def RateSentiment(sentiString):
    """Senti Strength java software to get sentiment from tweets"""

    # open a subprocess using shlex to get the command line string into the correct args list format
    p = subprocess.Popen(shlex.split("java -jar ../../cancer/SentiStrength.jar stdin explain sentidata ../../cancer/SentiStrength_Data/"),
                         stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    # communicate via stdin the string to be rated. Note that all spaces are replaced with +
    stdout_text, stderr_text = p.communicate(
        sentiString.replace(" ", "+").encode("utf-8"))
    if(stderr_text != False):
        print("Error rating sentiment with SentiStength")
    # remove the tab spacing between the positive and negative ratings. e.g. 1    -5 -> 1-5
    stdout_text = stdout_text.decode("utf-8").rstrip().replace("\t", "")
    return stdout_text[0], stdout_text[1:3]
