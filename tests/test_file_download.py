import os

from .config import DECISION_CC_WITH_FILE_ID, client

# from pyjudilibre.models import File


def test_download_file():
    decision = client.decision(decision_id=DECISION_CC_WITH_FILE_ID)

    assert isinstance(decision.files, list)

    for file in decision.files:
        filename = file.download()
        assert os.stat(filename)
        os.remove(filename)

    for file in decision.files:
        filename = file.download(filename="test.pdf")
        assert os.stat(filename)
        os.remove(filename)


def test_download_all_files():
    decision = client.decision(decision_id=DECISION_CC_WITH_FILE_ID)

    filenames = decision.download_all_files()
    for filename in filenames:
        assert os.stat(filename)
        os.remove(filename)
