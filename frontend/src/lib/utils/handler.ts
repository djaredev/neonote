import { handleError } from "./middlewares";

class Handler<T extends any[]> {
	private callback: ((...arg: T) => void | Promise<void>) | null;
	private restoreCallback: (...arg: T) => void | Promise<void>;
	constructor(callback: (...arg: T) => void) {
		this.callback = callback;
		this.restoreCallback = callback;
	}

	once = (...arg: T) => {
		this.callback?.(...arg);
		this.callback = null;
	};

	exec = async (...arg: T) => {
		try {
			await this.callback?.(...arg);
		} catch (error) {
			handleError(error);
		}
	};

	restore = () => {
		this.callback = this.restoreCallback;
	};

	clear = () => {
		this.callback = null;
	};
}

export default function handler<T extends any[]>(
	callback: (...arg: T) => void | Promise<void>,
	ref?: object
) {
	const instance = new Handler(callback.bind(ref));
	const callable = async (...arg: T) => {
		await instance.exec(...arg);
	};

	Object.assign(callable, instance);

	return callable as typeof callable & Handler<T>;
}
