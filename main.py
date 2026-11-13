"""news-image-01 entry: write the day's-news image to entry.png.

Contract (kit RULES.txt): the grader runs this file twice in a fresh
container and reads $MAKEFUN_OUTPUT_DIR/entry.png (default /output).
The file must be a complete PNG or JPEG, at most 1 MiB and at most
1024 by 1024 pixels, byte-identical across both runs. The image sits
beside this file in the repository and is copied verbatim.

The image sums up Friday 13 November 2026 in five captioned panels:
a night sky of 1,200 drones over Ukraine, the global Outlook outage
on its second day, mine fears in the Strait of Hormuz as oil slips,
the Assam highway crash, and the Nairobi building collapse. Facts
were cross-checked against Reuters, AP, AFP and BBC reporting of
that day, then re-checked against the evening wires after 13:35 UTC:
the Assam toll had risen from 23 to 26 dead (hospital confirmation
carried by PTI/The Hindu), so the Assam caption reads 26 DEAD; the
Nairobi toll stayed at 6 dead with all 405 workers accounted for;
the unconfirmed Hormuz tanker-explosion claim is deliberately NOT
depicted - only the mine threat and the falling oil price are.
"""

import hashlib
import os
import shutil
import struct

HERE = os.path.dirname(os.path.abspath(__file__))

# sha256 of the shipped entry.png. The gate is binary (a complete PNG
# or JPEG, at most 1 MiB, at most 1024 by 1024), so the copy is
# verified against the exact bytes that were judged locally: a
# truncated or swapped image must fail loudly here, not score 0.
EXPECTED_SHA256 = "96aeecb9b44a497d98ed58790c47bdb7d7be1b146eb86fee762e6394a8c83b29"
MAX_BYTES = 1048576


def main() -> None:
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    source = os.path.join(HERE, "entry.png")
    # Fail fast on a corrupted repo file instead of copying it first.
    source_data = open(source, "rb").read()
    assert hashlib.sha256(source_data).hexdigest() == EXPECTED_SHA256, "repo image bytes differ"
    assert len(source_data) <= MAX_BYTES, "repo image exceeds the 1 MiB cap"
    target = os.path.join(out_dir, "entry.png")
    shutil.copyfile(source, target)
    data = open(target, "rb").read()
    assert hashlib.sha256(data).hexdigest() == EXPECTED_SHA256, "copied image bytes differ"
    assert len(data) <= MAX_BYTES, "image exceeds the 1 MiB cap"
    assert data[:8] == b"\x89PNG\r\n\x1a\n", "shipped image is not the judged PNG"
    width, height = struct.unpack(">II", data[16:24])
    # The judged image is exactly 1024 by 1024; anything else means
    # a wrong file was shipped, so require the exact size, not just
    # the contract ceiling.
    assert (width, height) == (1024, 1024), "image is not 1024 by 1024"


if __name__ == "__main__":
    main()
