<script lang="ts">
	let { class: className = "", children, customCenter = undefined } = $props();
	import { onMount } from "svelte";
	import { setModalContext, getModalContext } from "./modal.svelte";
	// let modal: HTMLElement | null = null;

	setModalContext(customCenter);

	const modalState = getModalContext();

	onMount(() => {
		console.log("Modal mounted");
	});
</script>

<svelte:window onresize={modalState.onresize} />
<svelte:document
	onclick={modalState.isOpen ? modalState.onClose : null}
	onresize={modalState.onresize}
/>

<div
	class={className}
	bind:this={modalState.modal}
	onclick={!modalState.isOpen ? modalState.onOpen : null}
>
	{@render children()}
</div>
