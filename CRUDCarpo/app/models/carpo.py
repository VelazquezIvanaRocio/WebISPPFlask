from ..models.carrera import Carrera
from ..models.orientacion import Orientacion
from ..models.plan import Plan
class Carpo():
    def __init__(self, CarpoID, CarreraID, PlanDeEstudioID, OrientacionID, CarpoPrograma) -> None:
        self.CarpoID = CarpoID
        self.CarreraID = CarreraID
        self.PlanDeEstudioID = PlanDeEstudioID
        self.OrientacionID = OrientacionID
        self.CarpoPrograma = CarpoPrograma

    @classmethod
    def add_Carpo(self, mysql, CarreraID, PlanDeEstudioID, OrientacionID):
        try:
            cur = mysql.connection.cursor()
            if OrientacionID==False:
                sql = 'INSERT INTO Carpo(CarreraID,PlanDeEstudioID) VALUES (%s,%s)'
                cur.execute(sql, [CarreraID, PlanDeEstudioID])
            else:
                sql = 'INSERT INTO Carpo(CarreraID,PlanDeEstudioID,OrientacionID) VALUES (%s,%s,%s)'
                cur.execute(sql, [CarreraID, PlanDeEstudioID,
                        OrientacionID])
            mysql.connection.commit()
            return cur.lastrowid
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def get_Carpo_all(self, mysql):
        try:
            cur = mysql.connection.cursor()
            sql = 'SELECT * FROM Carpo'
            cur.execute(sql)
            Carpo = cur.fetchall()
            return Carpo
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def get_Carpo_id(self, mysql, CarpoID):
        try:
            cur = mysql.connection.cursor()
            sql = 'SELECT * from Carpo WHERE CarpoID=%s'
            cur.execute(sql, [CarpoID])
            Carpo = cur.fetchone()
            if Carpo:
                return Carpo
            else:
                return "vacio"

        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def delete_Carpo(self, mysql, CarpoID):
        try:
            cur = mysql.connection.cursor()
            sql = 'delete from Carpo where CarpoID = %s'
            cur.execute(sql, ([int(CarpoID)]))
            mysql.connection.commit()
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def search_carpo(self, mysql, CarreraID,OrientacionID,PlanID):
        try:
            cur=mysql.connection.cursor()
            if OrientacionID<1:
                sql='SELECT carpoid FROM carpo WHERE carreraid = %s AND plandeestudioid = %s'
                cur.execute(sql,[CarreraID,PlanID])
            else:
                sql = 'Select carpoid from carpo where carreraid = %s and plandeestudioid = %s and OrientacionID = %s'
                cur.execute(sql,[CarreraID,PlanID,OrientacionID])
            CarpoID = cur.fetchone()
            return CarpoID[0]
        except Exception as ex:
            raise Exception(ex)


    @classmethod
    def name_carpo(self,mysql,CarpoID):
        try:
            cur=mysql.connection.cursor()
            sql="SELECT CarreraNombre, OrientacionNombre, PlanNombre FROM (((carpo AS C left join carrera AS car ON C.CarreraID = car.CarreraID) inner join plandeestudio AS P ON C.PlanDeEstudioID = P.PlanID) LEFT join orientacion AS ori ON C.OrientacionID = ori.OrientacionID) WHERE C.CARPOID = %s;"
            cur.execute(sql,[CarpoID])
            nombre = cur.fetchone()
            return nombre 

        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def get_result_ori(self, mysql,carreraid):
        try:
            cur = mysql.connection.cursor()
            sql = 'SELECT orientacion.OrientacionID,orientacion.OrientacionNombre FROM carrera JOIN carpo ON carrera.carreraID= carpo.carreraID JOIN orientacion ON orientacion.OrientacionID = carpo.OrientacionID WHERE carrera.carreraID=%s'
            cur.execute(sql,[carreraid])
            ori = cur.fetchall()
            if len(ori)==0:
                ori=None
            return ori
        except Exception as ex:
            raise Exception(ex)
        
    @classmethod
    def get_ori_plan_carpo(self,mysql,carreraid):
        try:
            # First Fetch
            cur = mysql.connection.cursor()
            sql = 'select distinct plandeestudio.PlanNombre from carpo join carrera on carpo.carreraid = carrera.carreraID join plandeestudio on carpo.PlanDeEstudioID = PlanDeEstudio.planID where carpo.carreraid = %s'
            cur.execute(sql,[carreraid])
            plan = cur.fetchall()
            # Second Fetch
            sql = 'select orientacion.OrientacionNombre from carpo join carrera on carpo.carreraid = carrera.carreraID join orientacion on carpo.OrientacionID = orientacion.OrientacionID where carpo.carreraid = %s'
            cur.execute(sql,[carreraid])
            ori = cur.fetchall()
            return plan, ori
        except Exception as ex:
            raise Exception(ex)