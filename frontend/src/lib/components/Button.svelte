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
		background-color: #cdd6f4;
		border: none;
		color: #11111b;
		cursor: pointer;
		margin-top: 10px;
		padding: 10px;
		border-radius: 10px;
		font-size: 16px;

		&:hover {
			background-color: #bac2de;
		}

		&:active {
			transform: scale(0.98);
		}

		&:disabled {
			opacity: 0.5;
			cursor: not-allowed;

			&:hover {
				background-color: #cdd6f4;
			}

			&:active {
				transform: scale(1);
			}
		}
	}
</style>
