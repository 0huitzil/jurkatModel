!----------------------------------------------------------------------
!----------------------------------------------------------------------
!   Model2 :   Calcium exchange between the cytoplasm, ER, mitochondria and external medium via the PM
!----------------------------------------------------------------------
!----------------------------------------------------------------------
! PROGRAM model2
SUBROUTINE FUNC(NDIM,U,ICP,PAR,IJAC,F,DFDU,DFDP)
!     ---------- ----
      IMPLICIT NONE
      INTEGER, INTENT(IN) :: NDIM, ICP(*), IJAC
      DOUBLE PRECISION, INTENT(IN) :: U(NDIM), PAR(*)
      DOUBLE PRECISION, INTENT(OUT) :: F(NDIM)
      DOUBLE PRECISION, INTENT(INOUT) :: DFDU(NDIM,NDIM),DFDP(NDIM,*)
      ! Variables 
      DOUBLE PRECISION c, ce, h, Ct, s
      !Fluxes 
      DOUBLE PRECISION Jipr, Jserca
      DOUBLE PRECISION  Jh, Th
      ! Volume Parameters
      DOUBLE PRECISION delta, gamma
      ! IPR Parameters 
      DOUBLE PRECISION p, Kf, kbeta, Kp, Kc, Kh, Tmax, Kt
      DOUBLE PRECISION ma, A, B, ha, alpha, beta, P0 
      ! SERCA parameters 
      DOUBLE PRECISION Vs, Kbar, Ks, thaps, Jpm
      ! influx parameters 
      DOUBLE PRECISION a0
      ! PM parameters 
      DOUBLE PRECISION Vplc, Vdeg, Kdeg, Tp, Tg, s1, Vsoce, Ts, Ke, Vpm, Kpm
      DOUBLE PRECISION IPdeg, L, Jsoce, eps, PERIOD, TIME
      ! Variables 
      c=U(1)
      h=U(2)
      p=U(3)
      !======================================
      !Parameters 
      gamma=PAR(1)
      delta=PAR(2)
      Kf=PAR(3)
      kbeta=PAR(4)
      Kp=PAR(5)
      Kc=PAR(6)
      Kh=PAR(7)
      Tmax=PAR(8)
      Kt=PAR(9)
      Vs=PAR(10)
      PERIOD=PAR(11)
      Kbar=PAR(12)
      Ks=PAR(13)
      TIME=PAR(14)
      Vdeg=PAR(15)
      Kdeg=PAR(16)
      Vplc=PAR(17)
      Tp=PAR(18)
      s1=PAR(19)
      Vsoce=PAR(20)
      Ts=PAR(21)
      Ke=PAR(22)
      Vpm=PAR(23)
      Kpm=PAR(24)
      Ct=PAR(25)
      ! p=PAR(26)
      ce = gamma*(Ct-c)
      ! Conservation law 
      ! #======================================
      ! #IPR flux
      ma = c**4 / (Kc**4 + c**4)
      B = p**2 / (Kp**2 + p**2)
      A = 1 - p**2 / (Kp**2 + p**2)
      ha = Kh**4 / (Kh**4 + c**4)
      alpha = A*(1-ma*ha)
      beta = B*ma*h
      P0 = beta/(beta + kbeta*(beta + alpha))   
      Jipr=Kf*P0*(ce-c)
      ! #======================================
      ! #h fluxes
      Jh=(Kh**4 / (Kh**4 + c**4)) - h
      Th=Tmax* (Kt**4 / (Kt**4 + c**4))
      ! #======================================
      ! #SERCA flux
      Jserca=(Vs*(c**2 - Kbar*ce**2))/(c**2 + Ks**2)
      ! #======================================
      ! #IP3 flux
      IPdeg=Vdeg*c**2/(c**2+Kdeg**2)
      L=Vplc - IPdeg*p
      ! #======================================
      ! #PMCA flux
      ! Jpm = (Vpm*c**2)/(c**2 + Kpm**2)
      ! #======================================
      ! #SOCE flux
      ! Jsoce = Vsoce/(1+exp(s1*(ce-Ke)))
      ! #======================================
      !c
      F(1)=(Jipr - Jserca) 
      !h
      F(2)=Jh/Th
      !p
      F(3)=L/Tp
END SUBROUTINE FUNC

SUBROUTINE STPNT(NDIM,U,PAR,T)
!     ---------- -----
      IMPLICIT NONE
      INTEGER, INTENT(IN) :: NDIM
      DOUBLE PRECISION, INTENT(INOUT) :: U(NDIM),PAR(*)
      DOUBLE PRECISION, INTENT(IN) :: T
      ! Variables 
      DOUBLE PRECISION c, ce, h, Ct, s
      !Fluxes 
      DOUBLE PRECISION Jipr, Jserca
      DOUBLE PRECISION  Jh, Th
      ! Volume Parameters
      DOUBLE PRECISION delta, gamma
      ! IPR Parameters 
      DOUBLE PRECISION p, Kf, kbeta, Kp, Kc, Kh, Tmax, Kt
      DOUBLE PRECISION ma, A, B, ha, alpha, beta, P0 
      ! SERCA parameters 
      DOUBLE PRECISION Vs, Kbar, Ks, thaps, Jpm
      ! influx parameters 
      DOUBLE PRECISION a0
      ! PM parameters 
      DOUBLE PRECISION Vplc, Vdeg, Kdeg, Tp, Tg, s1, Vsoce, Ts, Ke, Vpm, Kpm
      DOUBLE PRECISION IPdeg, L, Jsoce, eps
      !======================================
      ! # PMCA 
      Vpm=3
      Kpm=0.2
      ! #======================================
      ! # SOCE 
      s1=0.2
      Vsoce=3
      Ts=15
      Ke=800   
      ! #======================================
      ! # IP3
      ! #Vplc=0.01 for burst, 0.005 for spike
      Vdeg=6
      Kdeg=0.5
      Vplc=0
      Tp=2
      ! p=0
      ! #======================================
      ! # General 
      gamma=5.5
      delta=2
      Ct=147
      ! #======================================
      ! # IPR 
      Kf=1.6
      kbeta=0.4
      Kp=10
      Kc=0.16
      ! #======================================
      ! # H 
      Kh=0.168
      Tmax=7.5
      Kt=0.095
      ! #======================================
      ! # SERCA 
      Vs=2
      Kbar=1e-08
      Ks=0.19
      !======================================
      PAR(1)=gamma
      PAR(2)=delta
      PAR(3)=Kf
      PAR(4)=kbeta
      PAR(5)=Kp
      PAR(6)=Kc
      PAR(7)=Kh
      PAR(8)=Tmax
      PAR(9)=Kt
      PAR(10)=Vs
      PAR(11)=0.0
      PAR(12)=Kbar
      PAR(13)=Ks
      PAR(14)=0.0
      PAR(15)=Vdeg
      PAR(16)=Kdeg
      PAR(17)=Vplc
      PAR(18)=Tp
      PAR(19)=s1
      PAR(20)=Vsoce
      PAR(21)=Ts
      PAR(22)=Ke
      PAR(23)=Vpm
      PAR(24)=Kpm
      PAR(25)=Ct
      PAR(26)=p
      !======================================
      U(1)=8.08056E-02
      U(2)=9.49198E-01
      U(3)=0
      ! U(3)=0.012
END SUBROUTINE STPNT

SUBROUTINE BCND
END SUBROUTINE BCND

SUBROUTINE ICND
END SUBROUTINE ICND

SUBROUTINE FOPT
END SUBROUTINE FOPT

SUBROUTINE PVLS(NDIM,U,PAR)
!     ---------- ----
      IMPLICIT NONE
      INTEGER, INTENT(IN) :: NDIM
      DOUBLE PRECISION, INTENT(IN) :: U(NDIM)
      DOUBLE PRECISION, INTENT(INOUT) :: PAR(*)
      ! Variables 
      DOUBLE PRECISION c, ce, h, Ct
      !Fluxes 
      DOUBLE PRECISION Jipr, Jserca
      DOUBLE PRECISION  Jh, Th, IPdeg, L
      ! Volume Parameters
      DOUBLE PRECISION gamma
      ! IPR Parameters 
      DOUBLE PRECISION p, Kf, kbeta, Kp, Kc, Kh, Tmax, Kt, Vplc
      DOUBLE PRECISION ma, A, B, ha, alpha, beta, P0, Vdeg, Kdeg, Tp
      ! SERCA parameters 
      DOUBLE PRECISION Vs, Kbar, Ks, thaps
      DOUBLE PRECISION, EXTERNAL :: GETP,GETU2
      PAR(45)=1/PAR(11)
      ! Set PAR(3) equal to the minimum of U(2)
      PAR(46)=GETP('MIN',1,U)
      PAR(47)=GETP('STA')
END SUBROUTINE PVLS

! END PROGRAM model2