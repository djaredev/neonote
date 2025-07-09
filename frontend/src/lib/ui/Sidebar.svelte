<script lang="ts">
	import { page } from "$app/state";
	import neonote from "$lib/icons/neonote.svg";
	import { ArchiveIcon, Trash2Icon, NotebookPenIcon, CirclePlusIcon } from "@lucide/svelte";
	import MakeNote from "./MakeNote.svelte";

	let { isOpen = $bindable(false) } = $props();

	let sidebar: HTMLElement;
	let isFixed = $derived.by(() => {
		if (isOpen && window.innerWidth < 745) {
			console.log("fixed");
			return true;
		}
		console.log("not fixed");
		return false;
	});

	function onClose() {
		if (!isFixed) return;
		isFixed = isOpen = false;
	}

	function onResize() {
		if (window.innerWidth < 745 && isOpen) {
			isOpen = false;
		}
	}
</script>

<svelte:window onresize={onResize} />

{#if isFixed}
	<div class="overlay-sidebar" onclick={onClose}></div>
{/if}

<nav class={["sidebar", isOpen && "sidebar-expanded"]} id="sidebar" bind:this={sidebar}>
	<div class="sidebar-header">
		<div class="sidebar-header-title">
			<img src={neonote} alt="Icono" width="40" height="40" />
			<span class="item-label">Neonote</span>
		</div>
	</div>
	<div class="sidebar-content">
		<div class="sidebar-group" onclick={onClose}>
			<div data-tooltip="Take a note">
				<MakeNote class="item">
					<div class="item-icon">
						<CirclePlusIcon size={34} color="#11111b" fill="#cdd6f4" />
					</div>
					<span class="item-label">Take a note</span>
				</MakeNote>
			</div>
		</div>
		<div class="sidebar-group">
			<a
				href="/"
				class="item {page.url.pathname === '/' && 'active'}"
				data-tooltip="Notes"
				data-sveltekit-preload-data="off"
				onclick={onClose}
			>
				<div class="item-icon">
					<NotebookPenIcon />
				</div>
				<span class="item-label">Notes</span>
			</a>
			<a
				href="/archive"
				class="item {page.url.pathname === '/archive' && 'active'}"
				data-tooltip="Archive"
				data-sveltekit-preload-data="off"
				onclick={onClose}
			>
				<div class="item-icon">
					<ArchiveIcon />
				</div>
				<span class="item-label">Archive</span>
			</a>
			<a
				href="/trash"
				class="item {page.url.pathname === '/trash' && 'active'}"
				data-tooltip="Trash"
				data-sveltekit-preload-data="off"
				onclick={onClose}
			>
				<div class="item-icon">
					<Trash2Icon />
				</div>
				<span class="item-label">Trash</span>
			</a>
		</div>
	</div>
</nav>

<style>
	* {
		margin: 0;
		padding: 0;
		box-sizing: border-box;
	}

	.active {
		background-color: #1e1e2e;
	}
	.sidebar {
		display: flex;
		flex-direction: column;
		align-items: flex-start;
		gap: 20px;
		width: 60px;
		padding: 10px;
		background: #11111b;
		color: #cdd6f4;
		outline: 1px solid #313244;
		/* transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275); */
		transition: all 0.3s cubic-bezier(0.175, 0.885, 0.12, 1.07);

		.sidebar-header {
			width: 100%;

			.sidebar-header-title {
				display: flex;
				align-items: center;
				gap: 10px;
				font-size: 24px;
				font-weight: bold;
				width: 100%;
				block-size: 50px;
			}
		}

		.sidebar-content {
			display: flex;
			flex-direction: column;
			flex: 1;
			gap: 50px;
			width: 100%;

			.sidebar-group {
				display: flex;
				flex-direction: column;
				gap: 10px;
				width: 100%;

				:global(.item) {
					display: flex;
					align-items: center;
					gap: 10px;
					text-decoration: none;
					border-radius: 10px;
				}

				:global(.item:hover) {
					background-color: #1e1e2e;
				}

				.item-icon {
					display: flex;
					justify-content: center;
					align-items: center;
					min-width: 40px;
					min-height: 40px;
					color: #cdd6f4;
				}
			}
		}

		:global(.sidebar-icon) {
			min-width: 24px;
			min-height: 24px;
		}

		.item-label {
			color: #cdd6f4;
			white-space: nowrap;
			overflow: hidden;
			transition: opacity 0.3s ease;
			opacity: 0;
		}

		&.sidebar-expanded {
			width: 180px;

			.item-label {
				opacity: 1;
			}
		}

		@media (width < 745px) {
			& {
				position: fixed;
				height: 100vh;
				transform: translateX(-100%);
				z-index: 1001;
				/* width: 0px; */
				/* display: none; */
			}

			&.sidebar-expanded {
				display: flex;
				transform: translateX(0);
			}
		}

		.sidebar-footer {
			width: 100%;
		}
	}

	:global(.overlay-sidebar) {
		position: fixed;
		top: 0;
		left: 0;
		width: 100%;
		height: 100%;
		background: rgba(0, 0, 0, 0.8);
		backdrop-filter: blur(5px);
		z-index: 1000;
		opacity: 1;
		transition: all 5s ease;
	}

	[data-tooltip] {
		position: relative;
		cursor: pointer;
		transition: all 0.3s ease;
	}

	[data-tooltip]::before {
		opacity: 0;
		visibility: hidden;
		position: absolute;
		pointer-events: none;
		transition: all 0.3s cubic-bezier(0.68, -0.55, 0.265, 1.55);
		transform: translateX(-10px);
		content: attr(data-tooltip);
		background: #11111b;
		color: #cdd6f4;
		font-size: 14px;
		padding: 12px 16px;
		border-radius: 10px;
		white-space: nowrap;
		left: calc(100% + 15px);
		top: 50%;
		transform: translateY(-50%) translateX(-10px);
		border: 1px solid #313244;
		box-shadow: 0 8px 25px rgba(0, 0, 0, 0.3);
		z-index: 1000;
	}

	.sidebar:not(.sidebar-expanded) [data-tooltip]:hover::before {
		opacity: 1;
		visibility: visible;
		transform: translateY(-50%) translateX(0);
	}

	@media (width < 500px) {
		[data-tooltip]::before {
			display: none;
		}
	}
</style>
