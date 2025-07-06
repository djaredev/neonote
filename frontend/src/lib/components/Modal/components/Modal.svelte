<script lang="ts">
	let { class: className = "", children, customCenter = undefined, onClose = undefined } = $props();
	import { setModalContext, getModalContext } from "./modal.svelte";
	// let modal: HTMLElement | null = null;

	setModalContext(customCenter);
	const modalState = getModalContext();
	modalState.onClose.clear();
</script>

<svelte:window onresize={modalState.onresize} />
<svelte:document onclick={(v) => modalState.onClose(v, onClose)} onresize={modalState.onresize} />

<div class={className} bind:this={modalState.modal} onclick={modalState.onOpen}>
	{@render children()}
</div>
