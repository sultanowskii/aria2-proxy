# aria2-proxy

`aria2` JSON-RPC proxy

The current main goal is to address [this issue](https://paper.seebug.org/120/) by making `dir` option more formalized and restricted. With `aria2-proxy`, you can specify a target directory whitelist (using env variable `ARIA2_PROXY_DIR_WHITELIST`, see [.env.example](.env.example)) - so that files could only be downloaded to these directories.

If proxy gets a RPC call containing `dir` option, it checks if specified `dir` is in the whitelist.

- If it is, the call is transparently proxied to the actual aria2 JSON-RPC server
- If it is not in the whitelist, error is returned

'Checked' methods:

- [`aria2.addUri`](https://aria2.github.io/manual/en/html/aria2c.html#aria2.addUri)
- [`aria2.addTorrent`](https://aria2.github.io/manual/en/html/aria2c.html#aria2.addTorrent)
- [`aria2.addMetalink`](https://aria2.github.io/manual/en/html/aria2c.html#aria2.addMetalink)
- [`aria2.changeOption`](https://aria2.github.io/manual/en/html/aria2c.html#aria2.changeOption)
- [`aria2.changeGlobalOption`](https://aria2.github.io/manual/en/html/aria2c.html#aria2.changeGlobalOption)
