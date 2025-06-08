<script lang="ts">
	import neonote from "$lib/icons/neonote.svg";
	import { ArchiveIcon, Trash2Icon, NotebookPenIcon, CirclePlusIcon } from "@lucide/svelte";

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
	<div class="overlay-view" onclick={onClose}></div>
{/if}

<nav class={["sidebar", isOpen && "sidebar-expanded"]} id="sidebar" bind:this={sidebar}>
	<div class="sidebar-header">
		<div class="sidebar-header-title">
			<img src={neonote} alt="Icono" width="50" height="50" />
			<span class="sidebar-label">Neonote</span>
		</div>
	</div>
	<div class="sidebar-content">
		<div class="sidebar-group">
			<div class="sidebar-link active" title="notes">
				<!-- <img src={newNote} alt="Icono" width="30" height="30" /> -->
				<CirclePlusIcon class="sidebar-icon" color="#cdd6f4" size={30} />
				<span class="sidebar-label">Take a note</span>
			</div>
		</div>
		<div class="sidebar-group">
			<a href="/" class="sidebar-link active" title="notes">
				<NotebookPenIcon class="sidebar-icon" color="#cdd6f4" size={30} />
				<span class="sidebar-label">Notes</span>
			</a>
			<a href="/archive" class="sidebar-link" title="archive">
				<ArchiveIcon class="sidebar-icon" color="#cdd6f4" size={30} />
				<span class="sidebar-label">Archive</span>
			</a>
			<a href="/trash" class="sidebar-link" title="trash">
				<Trash2Icon class="sidebar-icon" color="#cdd6f4" size={30} />
				<span class="sidebar-label">Trash</span>
			</a>
		</div>
	</div>
</nav>

<style>
	.sidebar {
		width: 50px;
		background-color: #11111b;
		padding: 10px;
		display: flex;
		flex-direction: column;
		align-items: flex-start;
		overflow: hidden;
		gap: 20px;
		border-right: 1px solid #313244;
		transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);

		/* border: 1px solid white; */
	}

	.sidebar-expanded {
		width: 200px;
		.sidebar-label {
			opacity: 1;
		}
	}

	.sidebar-header {
		width: 100%;
		/* border: 1px solid white; */
	}
	.sidebar-footer {
		width: 100%;
		color: #cdd6f4;
		/* border: 1px solid white; */
	}

	.sidebar-content {
		display: flex;
		width: 100%;
		flex-direction: column;
		gap: 50px;
		box-sizing: border-box;
		flex: 1;
		/* border: 1px solid white; */
	}

	.sidebar-link {
		color: #cdd6f4;
		display: flex;
		text-decoration: none;
		width: 100%;
		block-size: 50px;
		align-items: center;
		gap: 20px;
		outline: 2px solid transparent;
		border-radius: 10px;
		padding: 10px;
		box-sizing: border-box;
		/* border: 1px solid white; */
		overflow: hidden;
	}

	.sidebar-link:hover {
		background-color: #181825;
		color: #cdd6f4;
	}

	.sidebar-group {
		width: 100%;
		display: flex;
		gap: 10px;
		flex-direction: column;
		/* border: 1px solid white; */
	}

	.sidebar-header-title {
		color: #cdd6f4;
		font-size: 24px;
		font-weight: bold;
		/* padding-left: 20px; */
		display: flex;
		text-decoration: none;
		width: 100%;
		block-size: 50px;
		align-items: center;
		gap: 10px;
		outline: 2px solid transparent;
		border-radius: 10px;
		/* padding: 10px; */
		box-sizing: border-box;
	}

	.sidebar-label {
		white-space: nowrap;
		overflow: hidden;
		transition: opacity 0.3s ease;
		opacity: 0;
	}

	@media (width < 745px) {
		.sidebar {
			position: fixed;
			height: 100vh;
			transform: translateX(-100%);
			z-index: 1001;
			/* width: 0px; */
			/* display: none; */
		}

		.sidebar-expanded {
			display: flex;
			transform: translateX(0);
		}
	}

	:global(.overlay-view) {
		position: fixed;
		top: 0;
		left: 0;
		width: 100%;
		height: 100%;
		background: rgba(0, 0, 0, 0.8);
		backdrop-filter: blur(5px);
		/* display: flex; */
		/* align-items: center; */
		/* justify-content: center; */
		z-index: 1000;
		opacity: 1;
		/* visibility: hidden; */
		transition: all 5s ease;
	}

	:global(.sidebar-icon) {
		min-width: 30px;
	}
</style>
