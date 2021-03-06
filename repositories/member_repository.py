from db.run_sql import run_sql
from models.member import Member
from models.fitness_class import FitnessClass
import repositories.fitness_class_repository as fitness_class_repository

def save(member):
    sql = "INSERT INTO members (first_name, last_name, date_of_birth, membership_num, membership_type, is_active) VALUES (%s, %s, %s, %s, %s, %s) RETURNING id"
    values = [member.first_name, member.last_name, member.date_of_birth, member.membership_num, member.membership_type, member.is_active]
    results = run_sql(sql, values)
    id = results[0]['id']
    member.id = id
    return member

def select_all():
    members = []
    sql = "SELECT * FROM members"
    results = run_sql(sql)
    for result in results:
        member = Member(result["first_name"], result["last_name"], result["date_of_birth"], result["membership_num"], result["membership_type"], result["is_active"], result["id"])
        members.append(member)
    return members

def select(id):
    member = None
    sql = "SELECT * FROM members WHERE id = %s"
    values = [id]
    result = run_sql(sql, values)[0]
    if result is not None:
        member = Member(result['first_name'], result['last_name'], result['date_of_birth'], result['membership_num'], result["membership_type"], result["is_active"],  result['id'] )
    return member

def check_membership_num_exists(membership_num):
    sql = "SELECT * FROM members WHERE membership_num = %s"
    values = [membership_num]
    result = run_sql(sql, values)
    print("result is ", result)
    if result  == []:
        return False
    else:
        return True


def update(member):
    sql = "UPDATE members SET (first_name, last_name, date_of_birth, membership_num, membership_type, is_active) = (%s, %s, %s, %s, %s, %s) WHERE id = %s"
    values = [member.first_name, member.last_name, member.date_of_birth, member.membership_num, member.membership_type, member.is_active, member.id]
    run_sql(sql, values)
    return member


def bookings(member):
    fitness_classes = []
    bookings = []

    sql = "SELECT fitness_class_member_bookings.id AS booking_id, fitness_classes.* FROM fitness_classes INNER JOIN fitness_class_member_bookings ON fitness_class_member_bookings.fitness_class_id = fitness_classes.id WHERE member_id = %s"
    values = [member.id]
    results = run_sql(sql, values)
    for row in results:
        fitness_class = FitnessClass(row['title'], row['type'], row['duration'], row['discription'], row['id'] )
        fitness_classes.append(fitness_class)
        bookings.append(row['booking_id'])

    return (fitness_classes, bookings)


def delete_all():
    sql = "DELETE FROM members"
    run_sql(sql)


def delete(id):
    sql = "DELETE FROM members WHERE id = %s"
    values = [id]
    run_sql(sql, values)