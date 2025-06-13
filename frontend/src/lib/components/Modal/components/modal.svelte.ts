import { setContext, getContext, tick } from "svelte";
import handler from "$lib/utils/handler";
class ModalState {
	modal: HTMLElement | null = $state(null);
	isOpen: boolean = $state(false);
	view = $state<HTMLElement | null>(null);
	preview = $state<HTMLElement | null>(null);
	center = $state(false);
	ontransitionstart: ((event: TransitionEvent) => void) | null = null;
	ontransitionend: ((event: TransitionEvent) => void) | null = null;
	ontransitioncancel: ((event: TransitionEvent) => void) | null = null;
	resizeObserver = $state(false);
	overlay = $state(false);
	customCenter: ((width: number, heigth: number) => { left: number; top: number }) | undefined;
	constructor(customCenter?: (width: number, heigth: number) => { left: number; top: number }) {
		this.customCenter = customCenter;
	}

	onOpen = handler(() => {
		if (!this.preview || !this.modal) return;
		this.isOpen = this.overlay = true;
		this.onOpen.clear();
		tick().then(() => {
			tick().then(() => {
				if (!this.view || !this.preview || !this.modal) return;
				this.view.style.transition = "none";

				const width = this.view.offsetWidth;
				const height = this.view.offsetHeight;
				const rect = this.modal.getBoundingClientRect();

				this.moveView(rect.left, rect.top);
				this.resizeView(this.preview.offsetWidth, this.preview.offsetHeight);
				this.view.offsetHeight; // force reflow
				this.view.style.transition = "";

				tick().then(() => {
					if (!this.view || !this.preview) return;
					const { left, top } = this.calcenter(width, height);

					this.view.style.visibility = "visible";
					this.preview.style.visibility = "hidden";
					this.resizeView(width, height);
					this.moveView(left, top);
					this.waitForTransitions().then(() => {
						this.resizeObserver = this.center = true;
						this.resizeView(width, "auto");
						this.onClose.restore();
					});
				});
			});
		});
	}, this);

	onClose = handler((event: MouseEvent, callback) => {
		if (
			!this.preview ||
			!this.view ||
			this.preview.contains(event.target as Node) ||
			this.view.contains(event.target as Node)
		)
			return;
		this.onClose.clear();
		const rect = this.modal.getBoundingClientRect();
		this.overlay = this.resizeObserver = this.center = false;
		this.resizeView(this.view.offsetWidth, this.view.offsetHeight);
		this.resizeView(this.preview.offsetWidth, this.preview.offsetHeight);
		this.moveView(rect.left, rect.top);
		this.waitForTransitions().then(() => {
			if (this.preview) this.preview.style.visibility = "visible";
			this.isOpen = false;
			this.onOpen.restore();
			callback?.();
		});
	}, this);

	contentHeight = (cHeight: number) => {
		if (!this.view || !this.center) return;
		const { left, top } = this.calcenter(this.view.offsetWidth, this.view.offsetHeight);
		this.moveView(left, top);
	};

	onresize = () => {
		if (!this.view || !this.resizeObserver) return;
		const { left, top } = this.calcenter(this.view.offsetWidth, this.view.offsetHeight);
		this.moveView(left, top);
		if (this.view.offsetHeight > window.innerHeight) {
			this.view.style.height = "100vh";
		} else if (this.view.offsetHeight + 25 < window.innerHeight) {
			this.view.style.height = "auto";
		}
	};

	resizeView = (width: number, height: number | string) => {
		if (!this.view) return;
		this.view.style.width = `${width}px`;
		this.view.style.height = typeof height === "number" ? `${height}px` : height;
	};

	moveView = (left: number, top: number) => {
		if (!this.view) return;
		this.view.style.left = `${left}px`;
		this.view.style.top = `${top}px`;
	};

	waitForTransitions = (): Promise<void> => {
		return new Promise((resolve) => {
			let activeTransitions = 0;

			this.ontransitionstart = (event: TransitionEvent) => {
				if (event.target != this.view) return;
				activeTransitions++;
			};

			this.ontransitionend = (event: TransitionEvent) => {
				if (event.target != this.view) return;
				activeTransitions--;
				if (activeTransitions === 0) {
					this.ontransitionstart = this.ontransitionstart = this.ontransitionstart = null;
					resolve();
				}
			};

			this.ontransitioncancel = (event: TransitionEvent) => {
				if (event.target != this.view) return;
				this.ontransitionstart = this.ontransitionstart = this.ontransitionstart = null;
				resolve();
			};
		});
	};

	calcenter = (width: number, height: number) => {
		return this.customCenter
			? this.customCenter(width, height)
			: {
					left: (window.innerWidth - width) / 2,
					top: (window.innerHeight - height) / 2
				};
	};
}

const key = "modal";

export const setModalContext = (
	customCenter?: (width: number, heigth: number) => { left: number; top: number }
) => {
	setContext(key, new ModalState(customCenter));
};

export const getModalContext = () => {
	return getContext(key) as ModalState;
};
