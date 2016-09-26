window.onload = function(){	
	var winW = document.documentElement.clientWidth;
	var winH = document.documentElement.clientHeight;
	document.getElementsByTagName('html')[0].style.fontSize = winW / 3 +'px';


//商品分类图片自动居中	
	var oDiv = document.querySelectorAll('.spList li div');
	for(var i=0;i<oDiv.length;i++){
		oDiv[i].style.height = oDiv[i].offsetWidth+'px';
		oDiv[i].getElementsByTagName('img')[0].style.marginLeft = -oDiv[i].getElementsByTagName('img')[0].offsetWidth/2+'px';
	}
	
	
//商品详细页大图切换
	var presPos = 0;
	var changePos = 0;
	


	var aImg = document.querySelectorAll('.focus .bigImg p');
	var oUl = document.querySelectorAll('.focus .contrl ul');
	if(aImg.length > 1){
	for(var i=0;i<aImg.length;i++){
		aImg[i].index = i;
		aImg[i].addEventListener('touchstart',start,false);
		aImg[i].addEventListener('touchmove',move,false);
		aImg[i].addEventListener('touchend',end,false);
		
		var aLi = document.createElement('li');
		oUl[0].appendChild(aLi);
	}
	var aLi = document.querySelectorAll('.focus .contrl li');
	aLi[0].className = 'on';
	}	
	
	function start(e){
		this.startX = e.changedTouches[0].pageX;
	}
	function move(e){
		this.flag = true;
		e.preventDefault();
		var moveX = e.changedTouches[0].pageX;
		changePos = moveX - this.startX;
		cur = this.index;
		for(var i=0;i<aImg.length;i++){
			if(i!=cur){
				aImg[i].style.display = 'none';
			}			
			aImg[i].className = '';		
		}
		if(changePos > 0){  //往右
			this.pIndex = cur == 0 ? aImg.length-1 : cur - 1;
			presPos = -winW + changePos;
		}else if(changePos < 0){  //往左
			this.pIndex = cur == aImg.length-1 ? 0 : cur + 1;
			presPos = winW + changePos;
		}
		aImg[this.pIndex].className = 'zIndex';
		aImg[this.pIndex].style.display = 'block';
		aImg[cur].style.webkitTransform = 'translateX('+changePos+'px)';
		aImg[this.pIndex].style.webkitTransform = 'translateX('+presPos+'px)';


	}
	function end(e){
		if(this.flag){
			aImg[this.pIndex].style.webkitTransform = 'translateX(0)';
			aImg[this.pIndex].style.webkitTransition = '.2s';
			aImg[this.pIndex].addEventListener('webkitTransitionEnd',function(){
				this.style.webkitTransition = 'none';
			},false)
			for(var i=0;i<aLi.length;i++){
				aLi[i].className = '';
			}
			aLi[this.pIndex].className = 'on';
		}
		
	}







	
	
}