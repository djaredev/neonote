<script lang="ts">
	import { notify, NotificationLayout, NotificationType } from "$lib/state/notify.svelte";
	import {
		CircleCheckIcon,
		CircleXIcon,
		InfoIcon,
		TriangleAlertIcon,
		type Icon as IconType
	} from "@lucide/svelte";
	import { slide } from "svelte/transition";

	const icons: Record<NotificationType, typeof IconType> = {
		[NotificationType.Success]: CircleCheckIcon,
		[NotificationType.Info]: InfoIcon,
		[NotificationType.Error]: CircleXIcon,
		[NotificationType.Warning]: TriangleAlertIcon
	};
</script>

<div class="notify">
	{#each notify.notifications as notification (notification.id)}
		{@const Icon = icons[notification.notificationType]}
		<div class="notification {notification.notificationType}" transition:slide={{ duration: 200 }}>
			<div class="notification-header">
				<Icon />
				<span class="notification-title"
					>{notification.title ? notification.title : notification.notificationType}
				</span>
			</div>
			{#if notification.layoutType === NotificationLayout.Default}
				<div class="notification-content">{notification.message}</div>
				<div class="notification-footer">{notification.currentTime}</div>
			{/if}
		</div>
	{/each}
</div>

<style>
	* {
		box-sizing: border-box;
	}
	.notify {
		position: fixed;
		display: flex;
		flex-direction: column;
		gap: 10px;
		top: 20px;
		right: 20px;
		z-index: 2000;
		max-width: 400px;
		width: 100%;
		background: transparent;

		.notification {
			display: flex;
			flex-direction: column;
			gap: 10px;
			pointer-events: none;
			background: #181825;
			color: #cdd6f4;
			padding: 16px;
			border-radius: 10px;
			white-space: nowrap;
			border: 1px solid #313244;
			box-shadow: 0 8px 25px rgba(0, 0, 0, 0.3);

			.notification-header {
				display: flex;
				align-items: center;
				font-weight: bold;
				font-size: 16px;
				gap: 10px;
			}

			.notification-content {
				font-size: 14px;
			}

			.notification-footer {
				font-size: 12px;
				display: flex;
				justify-content: end;
			}

			&.Success {
				color: #a6e3a1;
			}

			&.Info {
				color: #89b4fa;
			}

			&.Error {
				color: #f38ba8;
			}

			&.Warning {
				color: #f9e2af;
			}
		}
	}
</style>
