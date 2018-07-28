# Development

**Ignore everything in this folder**, it is just a sandbox to play around in.


# ranmdisk

**i haven't tried this yet** ... it might be useful for unix domain socket
communications

create ramdisk on macOS with APFS

https://stackoverflow.com/questions/46224103/create-apfs-ram-disk-on-macos-high-sierra

```bash
hdid -nomount ram://<blocksize>
```

`<blocksize>` is 2048 * desired size in megabytes


one liner:

```bash
diskutil partitionDisk $(hdiutil attach -nomount ram://2048000) 1 GPTFormat APFS 'ramdisk' '100%'
```
