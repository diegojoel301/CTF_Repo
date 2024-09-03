// Adapted from https://github.com/faeldt/base64id

import * as crypto from "crypto";

class Base64Id {
	private bytesBuffer: Buffer | null;
	private bytesBufferIndex: number | null;
	private isGeneratingBytes: boolean;
	private sequenceNumber: number;

	public constructor() {
		this.bytesBuffer = null;
		this.bytesBufferIndex = null;
		this.isGeneratingBytes = false;
		this.sequenceNumber = 0;
	}

	private getRandomBytes(bytes: number = 12): Buffer {
		var BUFFER_SIZE = 4096
		var self = this;

		if (bytes > BUFFER_SIZE) {
			return crypto.randomBytes(bytes);
		}

		var bytesInBuffer = Math.floor(BUFFER_SIZE / bytes);
		var threshold = Math.floor(bytesInBuffer * 0.85);

		if (!threshold) {
			return crypto.randomBytes(bytes);
		}

		if (this.bytesBufferIndex == null) {
			this.bytesBufferIndex = -1;
		}

		if (this.bytesBufferIndex == bytesInBuffer) {
			this.bytesBuffer = null;
			this.bytesBufferIndex = -1;
		}

		// No buffered bytes available or index above threshold
		if (this.bytesBufferIndex == -1 || this.bytesBufferIndex > threshold) {
			if (!this.isGeneratingBytes) {
				this.isGeneratingBytes = true;
				crypto.randomBytes(BUFFER_SIZE, function(err, bytes) {
					self.bytesBuffer = bytes;
					self.bytesBufferIndex = 0;
					self.isGeneratingBytes = false;
				});
			}

			// Fall back to sync call when no buffered bytes are available
			if (this.bytesBufferIndex == -1) {
				return crypto.randomBytes(bytes);
			}
		}

		var result = this.bytesBuffer!.slice(bytes*this.bytesBufferIndex, bytes*(this.bytesBufferIndex+1));
		this.bytesBufferIndex++;

		return result;
	}

	public generateId(length: number = 15) {
		if (length % 3 != 0) {
			throw new Error("ID length must be a multiple of 3");
		}

		var rand = Buffer.alloc(length); // multiple of 3 for base64
		if (!rand.writeInt32BE) {
			return Math.abs(Math.random() * Math.random() * Date.now() | 0).toString()
			+ Math.abs(Math.random() * Math.random() * Date.now() | 0).toString();
		}
		this.sequenceNumber = (this.sequenceNumber + 1) | 0;
		rand.writeInt32BE(this.sequenceNumber, length - 4);
		this.getRandomBytes(length - 3).copy(rand);
		return rand.toString('base64').replace(/\//g, '_').replace(/\+/g, '-');
	}
}

const base64id = new Base64Id();

export default function generateId(length: number = 15) {
	return base64id.generateId(length);
}
