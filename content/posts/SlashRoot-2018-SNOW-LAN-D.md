+++
title = "SlashRoot 2018 - SNOW LAN(D)"
date = "2018-07-28 22:29:20"
categories = ["rev", "writeup"]
+++

> Download : [SNOW LAN(D).apk]()

## Analisa

Hal yang paling pertama yang dilakukan untuk memudahkan analisa game di android itu biasanya __identifikasi game engine__, _why?_ biar memudahkan reversing nantinya.
```
λ › unzip -l SNOW\ LAN\(D\).apk
...
    18432  07-24-2018 16:07   assets/bin/Data/Managed/Assembly-CSharp.dll
...
  1243616  01-01-1980 08:00   assets/bin/Data/sharedassets1.resource
    17916  05-09-2018 23:03   lib/armeabi-v7a/libmain.so
  3791288  05-09-2018 22:59   lib/armeabi-v7a/libmono.so
 18400572  05-09-2018 23:04   lib/armeabi-v7a/libunity.so
     6372  05-09-2018 23:03   lib/x86/libmain.so
  3656924  05-09-2018 23:03   lib/x86/libmono.so
 24043552  05-09-2018 23:08   lib/x86/libunity.so
...
```
Dari data file tersebut sudah bisa ditebak game menggunakan Unity Game Engine. Selanjutnya, _ngapain?_ Hampir semua logic dan kode utama game ada di `assets/bin/Data/Managed/Assembly-CSharp.dll`. File ini `.NET` dan bisa _didecompile_ dengan `dnSpy` atau sejenisnya.

Familiarisasi dengan game dengan memainkannya, ~~yo welkam bek wit mi~~. Ini foto dari _in-game_,

![]()

Mirip platformer 2d pada umumnya(?). Darah ada 3, kalau jatuh, tabrak monster, atau kena duri darah berkurang. Sudah agak kebayang sedikit dari tahun lalu, karena ini soal `joy` jadi cuma perlu menyelesaikan game ini.

## Pekalongan

![](https://i.imgflip.com/1qjm83.jpg)

YASHH!! It's cheating time boiz. Buka `Assembly-CSharp.dll` pake `dnSpy` (recommended punya editor _kodingan_ C# kalau belum terbiasa dengan MSIL). Platformer biar mudah selesainya, patch darah untuk gak berkurang. Fungsi yang lumayan bagus buat jadi awal carian itu biasanya Update untuk player controll.

```csharp
// PlayerController
// Token: 0x06000053 RID: 83 RVA: 0x00003180 File Offset: 0x00001380
private void FixedUpdate()
{
	if (this.curHealth > this.maxHealth)
	{
		this.curHealth = this.maxHealth;
	}
	if (this.curHealth <= 0)
	{
		this.Die();
	}
	if (!this.canMove)
	{
		return;
	}
	this.isGrounded = Physics2D.OverlapCircle(this.tagGround.position, this.radius, this.playerMask);
	this.myAnim.UpdateIsGrounded(this.isGrounded);
	if (Input.GetButtonDown("Jump"))
	{
		this.Jump();
	}
	this.Move(this.hInput);
}
```

`this.curHealth` bisa jadi indikator Health/darah Player, cari xrefs bisa lewat `Ctrl+Shift+R (Analyze)` > `Assigned by`, cari semua yang mengurangi darah Player, dan patch untuk tidak mengurangi sama sekali. Sedikit contoh, `duri.OnCollisionEnter2D`

```csharp
// duri
// Token: 0x06000025 RID: 37 RVA: 0x00002C10 File Offset: 0x00000E10
private void OnCollisionEnter2D(Collision2D col)
{
	if (col.transform.CompareTag("Player"))
	{
		this.jump.velocity.y = this.jump.jumpVelocity;
		this.jump.myBody.velocity = this.jump.velocity;
		this.jump.curHealth -= 2;
		this.blink.TriggerDamaged(this.jump.invicibleAfterDamaged);
	}
}
```

Patch/hapus bagian `this.jump.curHealth -= 2` serta yang lainnya, didapat mode `BAGUVIX`nya, hehe. Sedikit keluar dari bahas writeup, cara edit di `dnSpy` bisa pakai `Klik Kanan` > `Edit Method C#` > (kalau udah selesai edit) `Compile`. Kalau ada error? langsung edit `IL code` aja.

Lanjut, yang kedua ini agak unik karena saya sendiri gak terlalu jago untuk masalah ~~semua game~~ game seperti ini. Pas lagi bosen game ga selesai-selesai karena jatuh teruz muncul ide, ___Why not make this thing fly?___

Pada umumnya, algortima/logika untuk melompat di game itu seperti ini,
```C
if (!player->isJump) {
	// player can jump
} else {
	// player is already in jump state
}
```

Apa jadinya kalau `if (!player->isJump)` di paksa `true`? yep, Player bisa selalu melompat di udara dengan kondisi _"semi-flying state"_. Fungsi `PlayerController.Jump`,

```csharp
using System;
using UnityEngine;

// Token: 0x02000015 RID: 21
public partial class PlayerController : MonoBehaviour
{
	// Token: 0x06000056 RID: 86 RVA: 0x000032AC File Offset: 0x000014AC
	public void Jump()
	{
		if (this.isGrounded)
		{
			this.myBody.velocity += this.jumpVelocity * Vector2.up;
			this.playerJump.clip = this.jump;
			this.playerJump.Play();
		}
	}
}
```

Langsung di patch aja, hapus block `if (this.isGrounded)` atau paksa jadi true (`if(true)`).

Terakhir, tinggal repack, sign, dan install di Android. Mainkan gamenya.

## Demo

{% youtube AkmacOXBfko %}

## Flag

<center>`SlashRootCTF{ic3-L4n}`</center>
