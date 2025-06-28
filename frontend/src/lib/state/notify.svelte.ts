export enum NotificationType {
	Success = "Success",
	Info = "Info",
	Error = "Error",
	Warning = "Warning"
}

export enum NotificationLayout {
	Default = "Default",
	Minimal = "Minimal"
}

export type NotificationOptions = {
	title?: string;
	message?: string;
	layoutType?: NotificationLayout;
};

export type Notification = {
	id?: number;
	title?: string;
	message?: string;
	notificationType: NotificationType;
	layoutType: NotificationLayout;
	currentTime: string;
};

const createNotification = (
	notificationType: NotificationType,
	options: string | NotificationOptions
): Notification => {
	const newNotification = {
		notificationType: notificationType,
		layoutType: NotificationLayout.Default,
		currentTime: new Date().toLocaleTimeString()
	};

	if (typeof options === "string") {
		return {
			...newNotification,
			message: options
		};
	}

	return {
		...newNotification,
		...options
	};
};
class Notify {
	notifications = $state(new Array<Notification>());

	private show = (options: string | NotificationOptions, notificationType: NotificationType) => {
		const notification = createNotification(notificationType, options);
		this.add(notification);
		setTimeout(() => {
			this.remove(notification);
		}, 3000);
	};

	add = (notification: Notification) => {
		notification.id = this.notifications.length + 1;
		this.notifications.push(notification);
	};

	remove = (notification: Notification) => {
		this.notifications = this.notifications.filter((n) => n.id !== notification.id);
	};

	success = (options: string | NotificationOptions) => {
		this.show(options, NotificationType.Success);
	};

	info = (options: string | NotificationOptions) => {
		this.show(options, NotificationType.Info);
	};

	error = (options: string | NotificationOptions) => {
		this.show(options, NotificationType.Error);
	};

	warning = (options: string | NotificationOptions) => {
		this.show(options, NotificationType.Warning);
	};
}

export const notify = new Notify();
