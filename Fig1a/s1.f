* N players, reactive strategies
* one teacher

      program sab
      implicit real*8 (a-h,o-z)
      character*10 slurm
      
      parameter (o0=0.d+00,oh=0.5d+00,o1=1.d+00,o2=2.d+00)
      parameter (n=100,rn=dfloat(n),rrn=o1/rn,rrn1=o1/dfloat(n-1))
      parameter (u=0.1d+00*rrn,be=10.d+00,beta=be*rrn1)
      parameter (itend=10**5,init=itend/2)
      parameter (pt=0.9999d+00,qt=0.01d+00)
        
      dimension p(n),q(n),r(n),f(n),pn(n),qn(n)

      call get_command_argument(1,slurm)
      slurm=trim(adjustl(slurm))
      read(slurm,*) isl

      iseed=1000+isl
      call init_genrand(iseed)

      open (unit=3,file=slurm)

* different c values  

      isum=0

      do ic=2,10

      if (ic.lt.10) then
      c=dfloat(ic)*0.1d+00
      else
      c=0.95d+00
      endif 

      do irun=1,20
      isum=isum+1
      if (isl.eq.isum) goto 15
      enddo

      enddo

 15   continue

      m1=2

        
* initial population    

      z=o0
      eff=o0 
       
      p(1)=pt
      q(1)=qt
      r(1)=p(1)-q(1)
      
      do i=m1,n
      p(i)=genrand_real3()
      q(i)=genrand_real3()
      r(i)=p(i)-q(i)
      enddo 


* learning dynamics

      do it=1,itend 

* calculate payoff, do not play against self

      do i=1,n
      f(i)=o0
      enddo

      do i=1,n      
      do j=1,i-1      

      den=o1/(o1-r(i)*r(j))
      s1=(q(j)*r(i)+q(i))*den
      s2=(q(i)*r(j)+q(j))*den

      f(i)=f(i)+s2-c*s1
      f(j)=f(j)+s1-c*s2

      enddo
      enddo

* sample 

      if (it.gt.init) then
      z=z+o1
      do i=1,n      
      eff=eff+f(i)
      enddo
      endif

* update all players i=m1,n with PW comparison or mutation

      do i=m1,n 
  
      if (genrand_real3().lt.u) then 

      pn(i)=genrand_real3()      
      qn(i)=genrand_real3()      

      else 

      j = 1 + int(genrand_real3()*rn)

      prob=o1/(o1+dexp(-beta*(f(j)-f(i))))

      if (genrand_real3().lt.prob) then
      pn(i)=p(j)
      qn(i)=q(j)
      else     
      pn(i)=p(i)
      qn(i)=q(i)      
      endif

      endif

      enddo

* new generation i=m1,n

      do i=m1,n
      p(i)=pn(i)
      q(i)=qn(i)
      r(i)=p(i)-q(i)
      enddo
 
      enddo 

* output
      
      eff=eff*rrn*rrn1/z
      eff=eff/(o1-c)

      write (3,'(2f14.8)') c,eff
      call flush(3)

      stop
      end