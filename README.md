---
layout: post
title: "수면시간/패턴 측정(with.홈CCTV)"
subtitle: "Sleeptime/pattern measurement(with.CCTV in house)"
date: 2019-10-09
background: '/img/posts/bg-img/20.jpg'
comments: true
categories: Projects
---
<style>
	li {
		font-weight: bold;
	}
</style>
<h1 class="section-heading2" >작품소개</h1>
<p>라즈베리파이를 기반으로 한 홈 CCTV에 <a href="#motiondetection">동작 감지</a>를 통해 데이터를 수집하여 
스마트폰과 라즈베리파이를 블루투스를 통해 연동하여 라즈베리파이에 기록된 데이터를 기반으로 수면패턴을 
사용자에게 출력해주는 수면 보조 기구.
</p>

<div style="text-align: center;">
<img class="img-fluid" src="/img/posts/projects/sleeptight_RaspberryPi.PNG" align="center">
<span class="caption text-muted">
프로젝트에 사용된 라즈베리파이
</span>
</div>

<h2 class="section-heading2">개발배경 및 필요성</h2>

<ul>
	<li>개발배경</li>
	<p style="margin: 0;">OECD 통계에 따르면 한국인의 하루 평균 수면 시간은 7시간41분으로 회원국 중 
	최하위 이며 평균보다 40분이나 짧은 현대인들에게 좀 더 효율적인 수면 시간을 갖게 하기 위함.</p>
	<br>
	<li>필요성</li>
	<p style="margin: 0;">똑같은 수면을 하더라도 사람마다 숙면 정도가 다르기 때문에 수면 패턴을 
	안다면 자신의 수면 방해요소가 무엇인지 알 수 있고 그것을 해결함으로써 수면의 질이 높아져 사람에게 많은 이점을 가져다 줄 것으로 예상됨.</p>
	<br>
	<li>다른 제품과의 차별성</li>
	<p style="margin: 0;">시중에 출시된 Sleep Tech 제품(예 : 샤오미 밴드)들에 비해 <B>신체 부착</B>이나 <B>다른 필요한 조건</B>이 없으므로, 
	사용자는 일상생활에서 따로 신경을 쓰지 않아도 되며 제약없이 쉽고 편하게 사용이 가능함.</p>
	<br>
</ul>

<h3 class="section-heading2">시스템 구성</h3>

<img class="img-fluid" src="/img/posts/projects/sleeptight2.PNG" align="center">

<h4 class="section-heading2">S/W 기능</h4>

<ol>
	<li>수면패턴 측정</li>
		<p style="margin: 0;">자는 모습을 적외선 카메라로 촬영하고 영상처리를 이용하여 깊은 잠과 얕은 잠을 판별하여 수면패턴을 기록한다.</p>
		<br>
		<div style="text-align: center;">
		<img class="img-fluid" src="/img/posts/projects/sleeptight3.jpg" align="center">
		</div>
		<br>
	<li><a name="motiondetection">동작 감지</a></li>
		<p style="margin: 0;">카메라가 촬영하고 있을 때 설정된 영역에 움직임이 감지되면 동작 크기를 반환한다. 동작 크기에 따라 나타나는 면적이 커지고,
		이 데이터를 이용해 깊은 잠과 얕은 잠을 판별한다.</p>
		<br>
		<div style="text-align: center;">
		<img class="img-fluid" src="/img/posts/projects/sleeptight4.jpg" align="center">
		</div>
		<br>
	<li>수면 데이터 저장 및 표현</li>
		<p style="margin: 0;">카들어온 데이터를 분석하여 정보를 패턴별로 나눠 저장하고 Chart를 이용해 사용자 입장에서 보기 좋게 화면에 띄웠다.</p>
		<br>
		<div style="text-align: center;">
		<img class="img-fluid" src="/img/posts/projects/sleeptight5.jpg" align="center">
		</div>
		<br>
	<li>블루투스 통신</li>
		<p style="margin: 0;">앱과 라즈베리파이가 통신하도록 블루투스를 연결한다.</p>
		<br>
		<div style="text-align: center;">
		<img class="img-fluid" src="/img/posts/projects/sleeptight6.jpg" align="center">
		</div>
		<br>	
</ol>

<h4 class="section-heading2">H/W 기능</h4>

<ol>
	<li>조도 센서</li>
		<p style="margin: 0;">조도센서를 통해 빛의 밝기를 알 수 있다.</p>
		<br>
		<div style="text-align: center;">
		<img class="img-fluid" src="/img/posts/projects/sleeptight7.jpg" align="center">
		</div>
		<br>
	<li>적외선 카메라</li>
		<p style="margin: 0;">프로젝트 특성상 어두운 곳을 촬영해야 하기 때문에 적외선을 감지할 수 있는 카메라를 사용함.</p>
		<br>
		<div style="text-align: center;">
		<img class="img-fluid" src="/img/posts/projects/sleeptight8.jpg" align="center">
		</div>
		<br>
	<li>적외선 LED 램프</li>
		<p style="margin: 0;">적외선 카메라가 인식 할 수 있는 파장 850nm의 적외선을 촬영 대상에게 비추어 준다.</p>
		<br>
		<div style="text-align: center;">
		<img class="img-fluid" src="/img/posts/projects/sleeptight9.jpg" align="center">
		</div>
		<br>
</ol>

# 참고자료

- [소스 코드](https://github.com/bhsbhs235/sleeptight)






	