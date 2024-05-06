#!/bin/bash

product="unmusic"
productlow='unmusic'
arch="x86_64"
os="Linux" # Linux or Wine
oslow="linux"
glibc="2.36"
binariesdir="$HOME/binaries"
appimagedir="$binariesdir/appimage"
srcdir="$HOME/bin/$product/src"
resdir="$HOME/bin/$product/resources"
tmpdir="/tmp/$product"   # Will be deleted!
builddir="$tmpdir/build" # Will be deleted!
venv="$HOME/software/python/3.11.2_unmusic"

export "ARCH=$arch"

if [ ! -d "$venv" ]; then
    echo "Folder $venv does not exist!"; exit
fi

# Do this before `which pyinstaller`
source "$venv/bin/activate"

if [ "`which pyinstaller`" = "" ]; then
    echo "pyinstaller is not installed!"; exit
fi

if [ ! -d "$binariesdir/$product" ]; then
    echo "Folder $binariesdir/$product does not exist!"; exit
fi

if [ ! -d "$appimagedir" ]; then
    echo "Folder $appimagedir does not exist!"; exit
fi

if [ ! -d "$srcdir" ]; then
    echo "Folder $srcdir does not exist!"; exit
fi

if [ ! -d "$resdir" ]; then
    echo "Folder $resdir does not exist!"; exit
fi

if [ ! -e "$appimagedir/AppRun-$arch" ]; then
    echo "File $appimagedir/AppRun-$arch does not exist!"; exit
fi

if [ ! -e "$appimagedir/appimagetool-$arch.AppImage" ]; then
    echo "File $appimagedir/appimagetool-$arch.AppImage does not exist!"; exit
fi

if [ ! -e "$HOME/bin/$product/build/$os/$productlow.desktop" ]; then
    echo "File $HOME/bin/$product/build/$os/$productlow.desktop does not exist!"; exit
fi

if [ ! -e "$resdir/$productlow.png" ]; then
    echo "File $resdir/$productlow.png does not exist!"; exit
fi

# Build with pyinstaller
rm -rf "$tmpdir"
mkdir -p "$builddir" "$tmpdir/app/usr/bin" "$tmpdir/app/resources"
cp -r "$srcdir"/* "$builddir"
cp -r "$resdir" "$tmpdir/app"
cd "$builddir"
pyinstaller "$productlow.py"
# Create AppImage
mv "$builddir/dist/$productlow"/* "$tmpdir/app/usr/bin"
cd "$tmpdir/app"
cp "$appimagedir/AppRun-$arch" "$tmpdir/app/AppRun"
cp "$appimagedir/appimagetool-$arch.AppImage" "$tmpdir"
cp "$HOME/bin/$product/build/$os/$productlow.desktop" "$tmpdir/app"
cp "$resdir/$productlow.png" "$tmpdir/app"
cd "$tmpdir"
./appimagetool-$arch.AppImage app
read -p "Update the AppImage? (Y/n) " choice
if [ "$choice" = "n" ] || [ "$choice" = "N" ]; then
    exit;
fi
mv -fv "$tmpdir/$product-$arch.AppImage" "$HOME/binaries/$product/$productlow-$oslow-$arch-glibc$glibc.AppImage"
rm -rf "$tmpdir"
deactivate
