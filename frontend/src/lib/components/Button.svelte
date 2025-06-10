<script lang="ts">
	let { children, ...restProps } = $props();
</script>

<button class="button" {...restProps}>
	{@render children()}
</button>

<style>
	* {
		box-sizing: border-box;
	}
	.button {
		width: 80px;
		background-color: #cdd6f4;
		border: none;
		color: #11111b;
		cursor: pointer;
		margin-top: 10px;
		padding: 10px;
		border-radius: 10px;
		font-size: 16px;
	}

	.button:hover {
		background-color: #bac2de;
	}

	.button:active {
		transform: scale(0.98);
	}
</style>
