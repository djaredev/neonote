class Handler<T extends any[]> {
	private callback: ((...arg: T) => void) | null;
	private restoreCallback: (...arg: T) => void;
	constructor(callback: (...arg: T) => void) {
		this.callback = callback;
		this.restoreCallback = callback;
	}

	once = (...arg: T) => {
		this.callback?.(...arg);
		this.callback = null;
	};

	run = (...arg: T) => {
		this.callback?.(...arg);
	};

	restore = () => {
		this.callback = this.restoreCallback;
	};

	clear = () => {
		this.callback = null;
	};
}

export default function handler<T extends any[]>(callback: (...arg: T) => void, ref?: object) {
	return new Handler(callback.bind(ref));
}
